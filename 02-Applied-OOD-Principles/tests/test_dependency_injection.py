import inspect
from unittest import TestCase

from store.contracts import (
    DiscountCalculatorPort,
    EmailSender,
    OrderRepository,
    PaymentProcessorPort,
    ReceiptPresenter,
    ShippingCalculatorPort,
    SmsSender,
)
from store.main import build_demo_service, build_payment_registry
from store.models import Order, OrderItem
from store.notification import NotificationService, SmsOnlyNotifier
from store.order_service import OrderService
from store.payment import PaymentProcessor
from store.pricing import DiscountCalculator, ShippingCalculator
from store.receipt import ReceiptPrinter
from store.storage import MySqlDatabase

from test_characterization import capture_stdout, make_regular


class FakeDiscountCalculator:
    def __init__(self, discount=0.0):
        self.discount = discount
        self.calls = []

    def calculate(self, order):
        self.calls.append(order)
        return self.discount


class FakePaymentProcessor:
    def __init__(self, receipt="fake_receipt"):
        self.receipt = receipt
        self.calls = []

    def process(self, order, amount):
        self.calls.append((order, amount))
        return self.receipt


class FakeShippingCalculator:
    def __init__(self, shipping=5.0):
        self.shipping = shipping
        self.calls = []

    def calculate(self, subtotal):
        self.calls.append(subtotal)
        return self.shipping


class FakeEmailSender:
    def __init__(self):
        self.calls = []

    def send_email(self, customer, message):
        self.calls.append((customer, message))


class FakeSmsSender:
    def __init__(self):
        self.calls = []

    def send_sms(self, customer, message):
        self.calls.append((customer, message))


class FakeOrderRepository:
    def __init__(self):
        self.saved = []

    def save_order(self, order):
        self.saved.append(order)


class FakeReceiptPrinter:
    def __init__(self):
        self.calls = []

    def print_receipt(self, order, subtotal, discount, shipping, total, receipt):
        self.calls.append((order, subtotal, discount, shipping, total, receipt))


def make_fakes(discount=0.0, shipping=5.0):
    return {
        "discount_calculator": FakeDiscountCalculator(discount),
        "shipping_calculator": FakeShippingCalculator(shipping),
        "payment_processor": FakePaymentProcessor(),
        "email_sender": FakeEmailSender(),
        "sms_sender": FakeSmsSender(),
        "database": FakeOrderRepository(),
        "receipt_printer": FakeReceiptPrinter(),
    }


def own_protocol_methods(protocol):
    return {
        name
        for name, value in vars(protocol).items()
        if callable(value) and not name.startswith("_")
    }


class ConstructorRequiresCollaboratorsTests(TestCase):
    def test_signature_exposes_exactly_the_required_collaborators(self):
        parameters = inspect.signature(OrderService.__init__).parameters
        self.assertEqual(
            list(parameters),
            [
                "self",
                "discount_calculator",
                "shipping_calculator",
                "payment_processor",
                "email_sender",
                "sms_sender",
                "database",
                "receipt_printer",
            ],
        )

    def test_constructing_without_collaborators_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderService()

    def test_each_missing_collaborator_raises_type_error(self):
        for missing in (
            "discount_calculator",
            "shipping_calculator",
            "payment_processor",
            "email_sender",
            "sms_sender",
            "database",
            "receipt_printer",
        ):
            with self.subTest(missing=missing):
                kwargs = make_fakes()
                del kwargs[missing]
                with self.assertRaises(TypeError):
                    OrderService(**kwargs)

    def test_service_stores_each_injected_collaborator_as_an_attribute(self):
        kwargs = make_fakes()
        service = OrderService(**kwargs)
        for attribute, fake in kwargs.items():
            self.assertIs(getattr(service, attribute), fake)


class InjectedFakeOrchestrationTests(TestCase):
    def setUp(self):
        self.fakes = make_fakes(discount=6.0)
        self.service = OrderService(**self.fakes)
        self.customer = make_regular()
        self.order = Order(
            id=401,
            customer=self.customer,
            payment_method="paypal",
            items=[OrderItem(6, "Gadget", 30.00, 2)],
        )

    def test_checkout_flows_through_injected_fakes_with_computed_total(self):
        returned, output = capture_stdout(self.service.process_order, self.order)

        self.assertIs(returned, self.order)
        self.assertEqual(self.fakes["discount_calculator"].calls, [self.order])
        payment_calls = self.fakes["payment_processor"].calls
        self.assertEqual(payment_calls, [(self.order, 59.0)])
        self.assertEqual(self.order.status, "paid")
        self.assertEqual(self.fakes["database"].saved, [self.order])
        expected_message = "Order 401 total $59.00 (fake_receipt)"
        self.assertEqual(
            self.fakes["email_sender"].calls,
            [(self.customer, expected_message)],
        )
        self.assertEqual(
            self.fakes["sms_sender"].calls,
            [(self.customer, expected_message)],
        )
        self.assertEqual(
            self.fakes["receipt_printer"].calls,
            [(self.order, 60.0, 6.0, 5.0, 59.0, "fake_receipt")],
        )

    def test_service_delegates_exactly_one_print_receipt_call(self):
        capture_stdout(self.service.process_order, self.order)

        self.assertEqual(len(self.fakes["receipt_printer"].calls), 1)

    def test_receipt_block_is_still_rendered_by_the_real_presenter(self):
        service = OrderService(
            discount_calculator=self.fakes["discount_calculator"],
            shipping_calculator=self.fakes["shipping_calculator"],
            payment_processor=self.fakes["payment_processor"],
            email_sender=self.fakes["email_sender"],
            sms_sender=self.fakes["sms_sender"],
            database=self.fakes["database"],
            receipt_printer=ReceiptPrinter(),
        )
        _, output = capture_stdout(service.process_order, self.order)

        self.assertEqual(
            output,
            "--- Receipt for order 401 ---\n"
            "  Gadget               x2  $60.00\n"
            "  Subtotal    $60.00\n"
            "  Discount   -$6.00\n"
            "  Shipping    $5.00\n"
            "  TOTAL       $59.00\n"
            "  Payment     fake_receipt\n",
        )

    def test_notify_false_reaches_neither_channel_but_still_charges_and_saves(self):
        capture_stdout(self.service.process_order, self.order, notify=False)

        self.assertEqual(self.fakes["email_sender"].calls, [])
        self.assertEqual(self.fakes["sms_sender"].calls, [])
        self.assertEqual(len(self.fakes["payment_processor"].calls), 1)
        self.assertEqual(self.fakes["database"].saved, [self.order])

    def test_invalid_order_is_rejected_before_any_collaborator_is_used(self):
        empty = Order(id=402, customer=self.customer)

        with self.assertRaises(ValueError):
            capture_stdout(self.service.process_order, empty)

        self.assertEqual(self.fakes["discount_calculator"].calls, [])
        self.assertEqual(self.fakes["payment_processor"].calls, [])
        self.assertEqual(self.fakes["database"].saved, [])
        self.assertEqual(self.fakes["receipt_printer"].calls, [])


class StructuralConformanceTests(TestCase):
    def test_concrete_collaborators_satisfy_their_structural_contracts(self):
        notification = NotificationService()
        self.assertIsInstance(DiscountCalculator(), DiscountCalculatorPort)
        self.assertIsInstance(ShippingCalculator(), ShippingCalculatorPort)
        self.assertIsInstance(
            PaymentProcessor(build_payment_registry()), PaymentProcessorPort
        )
        self.assertIsInstance(notification, EmailSender)
        self.assertIsInstance(notification, SmsSender)
        self.assertIsInstance(MySqlDatabase(), OrderRepository)
        self.assertIsInstance(SmsOnlyNotifier(), SmsSender)
        self.assertIsInstance(ReceiptPrinter(), ReceiptPresenter)

    def test_each_contract_declares_only_the_method_order_service_calls(self):
        self.assertEqual(own_protocol_methods(DiscountCalculatorPort), {"calculate"})
        self.assertEqual(own_protocol_methods(ShippingCalculatorPort), {"calculate"})
        self.assertEqual(own_protocol_methods(PaymentProcessorPort), {"process"})
        self.assertEqual(own_protocol_methods(EmailSender), {"send_email"})
        self.assertEqual(own_protocol_methods(SmsSender), {"send_sms"})
        self.assertEqual(own_protocol_methods(OrderRepository), {"save_order"})
        self.assertEqual(own_protocol_methods(ReceiptPresenter), {"print_receipt"})


class CompositionRootWiringTests(TestCase):
    def test_demo_service_wires_real_collaborators(self):
        service = build_demo_service()

        self.assertIsInstance(service.discount_calculator, DiscountCalculator)
        self.assertIsInstance(service.shipping_calculator, ShippingCalculator)
        self.assertIsInstance(service.payment_processor, PaymentProcessor)
        self.assertIsInstance(service.email_sender, NotificationService)
        self.assertIsInstance(service.sms_sender, NotificationService)
        self.assertIsInstance(service.database, MySqlDatabase)
        self.assertIsInstance(service.receipt_printer, ReceiptPrinter)

    def test_demo_service_shares_one_notification_instance_for_both_channels(self):
        service = build_demo_service()
        self.assertIs(service.email_sender, service.sms_sender)
