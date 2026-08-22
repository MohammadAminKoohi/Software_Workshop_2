from unittest import TestCase

from store.main import build_demo_orders, main
from store.models import Order, OrderItem
from store.receipt import ReceiptPrinter

import test_characterization
from test_characterization import capture_stdout, make_regular


class ReceiptFormattingTests(TestCase):
    def setUp(self):
        self.printer = ReceiptPrinter()

    def test_simple_receipt_preserves_every_line_and_spacing(self):
        order = Order(
            id=601,
            customer=make_regular(),
            payment_method="paypal",
            items=[OrderItem(6, "Gadget", 30.00, 2),
                   OrderItem(7, "Tiny", 1.00, 1)],
        )

        _, output = capture_stdout(
            self.printer.print_receipt,
            order,
            60.00,
            6.00,
            7.25,
            61.25,
            "paid_by_paypal:61.25",
        )

        self.assertEqual(
            output,
            "--- Receipt for order 601 ---\n"
            "  Gadget               x2  $60.00\n"
            "  Tiny                 x1  $1.00\n"
            "  Subtotal    $60.00\n"
            "  Discount   -$6.00\n"
            "  Shipping    $7.25\n"
            "  TOTAL       $61.25\n"
            "  Payment     paid_by_paypal:61.25\n",
        )

    def test_bundle_receipt_has_no_item_lines_and_zero_subtotal(self):
        _, _, bundle = build_demo_orders()

        _, output = capture_stdout(
            self.printer.print_receipt,
            bundle,
            0.00,
            0.00,
            5.00,
            5.00,
            "paid_by_credit_card:5.00",
        )

        self.assertEqual(
            output,
            "--- Receipt for order 103 ---\n"
            "  Subtotal    $0.00\n"
            "  Discount   -$0.00\n"
            "  Shipping    $5.00\n"
            "  TOTAL       $5.00\n"
            "  Payment     paid_by_credit_card:5.00\n",
        )


class PresenterDelegationTests(TestCase):
    def test_service_passes_priced_values_to_injected_presenter_in_order(self):
        events = []

        class RecordingDiscount:
            def calculate(self, order):
                events.append("discount")
                return 6.0

        class RecordingShipping:
            def calculate(self, subtotal):
                events.append("shipping")
                return 5.0

        class RecordingPayment:
            def process(self, order, amount):
                events.append("payment")
                return "fake_receipt"

        class RecordingRepository:
            def save_order(self, order):
                events.append("save")

        class RecordingEmail:
            def send_email(self, customer, message):
                events.append("email")

        class RecordingSms:
            def send_sms(self, customer, message):
                events.append("sms")

        from store.order_service import OrderService

        presenter_calls = []

        class RecordingPresenter:
            def print_receipt(self, order, subtotal, discount, shipping, total, receipt):
                events.append("receipt")
                presenter_calls.append(
                    (order, subtotal, discount, shipping, total, receipt)
                )

        service = OrderService(
            discount_calculator=RecordingDiscount(),
            shipping_calculator=RecordingShipping(),
            payment_processor=RecordingPayment(),
            email_sender=RecordingEmail(),
            sms_sender=RecordingSms(),
            database=RecordingRepository(),
            receipt_printer=RecordingPresenter(),
        )
        order = Order(
            id=401,
            customer=make_regular(),
            payment_method="paypal",
            items=[OrderItem(6, "Gadget", 30.00, 2)],
        )

        returned, _ = capture_stdout(service.process_order, order)

        self.assertIs(returned, order)
        self.assertEqual(
            events,
            ["discount", "shipping", "payment", "save", "email", "sms", "receipt"],
        )
        self.assertEqual(presenter_calls, [(order, 60.0, 6.0, 5.0, 59.0, "fake_receipt")])


class DemoOrderingTests(TestCase):
    def test_full_demo_output_remains_byte_identical_after_extraction(self):
        _, output = capture_stdout(main)
        self.assertEqual(
            output,
            test_characterization.DemoStdoutCharacterizationTests.EXPECTED_DEMO_OUTPUT,
        )
