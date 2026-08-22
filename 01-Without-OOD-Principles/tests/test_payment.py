import io
import unittest
from contextlib import redirect_stdout

from store.models import Customer, Order, OrderItem
from store.payment import PaymentProcessor


def make_order(payment_method: str) -> Order:
    customer = Customer(
        id=1,
        name="Alice",
        email="alice@example.com",
        phone="555-0100",
        credit_card="4111 1111 1111 1111",
        bitcoin_address="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    )
    return Order(
        id=101,
        customer=customer,
        payment_method=payment_method,
        items=[OrderItem(1, "Laptop", 999.99, 1)],
    )


class CashPaymentTest(unittest.TestCase):
    def setUp(self):
        self.processor = PaymentProcessor()

    def test_cash_returns_receipt(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            result = self.processor.process(make_order("cash"), 123.456)
        self.assertEqual(result, "paid_by_cash:123.46")
        self.assertEqual(buffer.getvalue(), "[payment] Receiving cash 123.46\n")

    def test_cash_prints_console_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.processor.process(make_order("cash"), 42.0)
        self.assertEqual(buffer.getvalue(), "[payment] Receiving cash 42.00\n")


class ExistingPaymentRegressionTest(unittest.TestCase):
    def setUp(self):
        self.processor = PaymentProcessor()

    def test_credit_card_receipt_and_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            result = self.processor.process(make_order("credit_card"), 25.0)
        self.assertEqual(result, "paid_by_credit_card:25.00")
        self.assertEqual(
            buffer.getvalue(), "[payment] Charging card 4111 1111 1111 1111 25.00\n"
        )

    def test_paypal_receipt_and_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            result = self.processor.process(make_order("paypal"), 30.0)
        self.assertEqual(result, "paid_by_paypal:30.00")
        self.assertEqual(
            buffer.getvalue(), "[payment] Charging PayPal alice@example.com 30.00\n"
        )

    def test_bitcoin_receipt_and_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            result = self.processor.process(make_order("bitcoin"), 40.0)
        self.assertEqual(result, "paid_by_bitcoin:40.00")
        self.assertEqual(
            buffer.getvalue(),
            "[payment] Charging BTC 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa 40.00\n",
        )


class UnknownPaymentMethodTest(unittest.TestCase):
    def test_unknown_method_raises_value_error(self):
        processor = PaymentProcessor()
        with self.assertRaises(ValueError) as ctx:
            processor.process(make_order("barter"), 10.0)
        self.assertIn("'barter'", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
