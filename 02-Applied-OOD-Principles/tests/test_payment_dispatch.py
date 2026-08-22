from unittest import TestCase

from store.main import build_payment_registry
from store.models import Order, OrderItem
from store.payment import PaymentProcessor

from test_characterization import capture_stdout, make_regular, make_vip


class ExistingPaymentHandlerTests(TestCase):
    def setUp(self):
        self.processor = PaymentProcessor(build_payment_registry())

    def test_credit_card_output_and_receipt_are_preserved(self):
        order = Order(
            id=701,
            customer=make_vip(),
            payment_method="credit_card",
            items=[OrderItem(1, "Item", 1.0, 1)],
        )

        receipt, output = capture_stdout(self.processor.process, order, 12.5)

        self.assertEqual(output, "[payment] Charging card 4111 1111 1111 1111 12.50\n")
        self.assertEqual(receipt, "paid_by_credit_card:12.50")

    def test_paypal_output_and_receipt_are_preserved(self):
        order = Order(
            id=702,
            customer=make_regular(),
            payment_method="paypal",
            items=[OrderItem(1, "Item", 1.0, 1)],
        )

        receipt, output = capture_stdout(self.processor.process, order, 7.0)

        self.assertEqual(output, "[payment] Charging PayPal bob@example.com 7.00\n")
        self.assertEqual(receipt, "paid_by_paypal:7.00")

    def test_bitcoin_output_and_receipt_are_preserved(self):
        order = Order(
            id=703,
            customer=make_regular(bitcoin_address="1AbcDef"),
            payment_method="bitcoin",
            items=[OrderItem(1, "Item", 1.0, 1)],
        )

        receipt, output = capture_stdout(self.processor.process, order, 3.25)

        self.assertEqual(output, "[payment] Charging BTC 1AbcDef 3.25\n")
        self.assertEqual(receipt, "paid_by_bitcoin:3.25")

    def test_unknown_method_error_is_preserved_exactly(self):
        order = Order(
            id=704,
            customer=make_regular(),
            payment_method="barter",
            items=[OrderItem(1, "Item", 1.0, 1)],
        )

        with self.assertRaises(ValueError) as context:
            self.processor.process(order, 1.0)

        self.assertEqual(str(context.exception), "Unknown payment method: 'barter'")


class PaymentExtensionBoundaryTests(TestCase):
    def test_synthetic_handler_extends_dispatch_without_processor_changes(self):
        calls = []

        class TestOnlyHandler:
            def process(self, order, amount):
                calls.append((order, amount))
                return f"paid_by_test_handler:{amount:.2f}"

        processor = PaymentProcessor({"test_only": TestOnlyHandler()})
        order = Order(
            id=705,
            customer=make_regular(),
            payment_method="test_only",
            items=[OrderItem(1, "Item", 1.0, 1)],
        )

        receipt = processor.process(order, 9.75)

        self.assertEqual(calls, [(order, 9.75)])
        self.assertEqual(receipt, "paid_by_test_handler:9.75")

    def test_processor_requires_registry_and_copies_input_mapping(self):
        with self.assertRaises(TypeError):
            PaymentProcessor()

        handlers = {}
        processor = PaymentProcessor(handlers)
        handlers["late"] = object()
        order = Order(
            id=706,
            customer=make_regular(),
            payment_method="late",
            items=[OrderItem(1, "Item", 1.0, 1)],
        )

        with self.assertRaisesRegex(ValueError, "Unknown payment method: 'late'"):
            processor.process(order, 1.0)
