from unittest import TestCase

from store.main import build_demo_orders
from store.models import Order, OrderItem
from store.notification import NotificationService
from store.order_service import OrderService
from store.payment import PaymentProcessor
from store.pricing import ShippingCalculator
from store.storage import MySqlDatabase

from test_characterization import capture_stdout, make_default_service, make_regular, make_vip
from test_dependency_injection import FakeDiscountCalculator, FakePaymentProcessor


class ShippingRuleBoundaryTests(TestCase):
    def setUp(self):
        self.calculator = ShippingCalculator()

    def test_shipping_is_five_dollars_immediately_below_threshold(self):
        self.assertEqual(self.calculator.calculate(99.99), 5.0)
        self.assertIsInstance(self.calculator.calculate(99.99), float)

    def test_shipping_is_free_exactly_at_threshold(self):
        self.assertEqual(self.calculator.calculate(100.00), 0.0)
        self.assertIsInstance(self.calculator.calculate(100.00), float)

    def test_shipping_is_free_immediately_above_threshold(self):
        self.assertEqual(self.calculator.calculate(100.01), 0.0)
        self.assertIsInstance(self.calculator.calculate(100.01), float)


class FixedShippingCalculator:
    def __init__(self, value):
        self.value = value
        self.calls = []

    def calculate(self, subtotal):
        self.calls.append(subtotal)
        return self.value


class ShippingInjectionTests(TestCase):
    def test_service_uses_injected_shipping_value_not_a_hidden_rule(self):
        shipping = FixedShippingCalculator(7.25)
        service = OrderService(
            discount_calculator=FakeDiscountCalculator(6.0),
            shipping_calculator=shipping,
            payment_processor=FakePaymentProcessor(),
            email_sender=NotificationService(),
            sms_sender=NotificationService(),
            database=MySqlDatabase(),
        )
        order = Order(
            id=501,
            customer=make_regular(),
            payment_method="paypal",
            items=[OrderItem(6, "Gadget", 30.00, 2)],
        )

        _, output = capture_stdout(service.process_order, order)

        self.assertEqual(shipping.calls, [60.0])
        self.assertIn("  Discount   -$6.00", output)
        self.assertIn("  Shipping    $7.25", output)
        self.assertIn("  TOTAL       $61.25", output)


class EndToEndTotalsUnchangedTests(TestCase):
    def test_simple_vip_order_total_stays_eight_hundred_nineteen_ninety_nine(self):
        service = make_default_service()
        order = Order(
            id=101,
            customer=make_vip(),
            payment_method="credit_card",
            items=[OrderItem(1, "Laptop", 999.99, 1),
                   OrderItem(2, "Mouse", 25.00, 1)],
        )

        returned, output = capture_stdout(service.process_order, order)

        self.assertIs(returned, order)
        self.assertIn("paid_by_credit_card:819.99", output)
        self.assertIn("  TOTAL       $819.99", output)

    def test_bundle_total_stays_five_dollars(self):
        service = make_default_service()
        _, _, bundle = build_demo_orders()

        returned, output = capture_stdout(service.process_order, bundle)

        self.assertIs(returned, bundle)
        self.assertIn("paid_by_credit_card:5.00", output)
        self.assertIn("  Shipping    $5.00", output)
        self.assertIn("  TOTAL       $5.00", output)
