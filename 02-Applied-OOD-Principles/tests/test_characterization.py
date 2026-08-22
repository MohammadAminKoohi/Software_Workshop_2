import io
from contextlib import redirect_stdout
from unittest import TestCase

from store.main import build_demo_orders, main
from store.models import BundleOrder, Customer, Order, OrderItem
from store.notification import NotificationService, SmsOnlyNotifier
from store.order_service import OrderService
from store.payment import PaymentProcessor
from store.pricing import DiscountCalculator
from store.storage import MySqlDatabase


def capture_stdout(callable_obj, *args, **kwargs):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = callable_obj(*args, **kwargs)
    return result, buffer.getvalue()


def make_vip(**overrides):
    fields = dict(
        id=1,
        name="Alice",
        email="alice@example.com",
        phone="555-0100",
        is_vip=True,
        address="1 Main St",
        credit_card="4111 1111 1111 1111",
        bitcoin_address="bc1qxyz",
    )
    fields.update(overrides)
    return Customer(**fields)


def make_regular(**overrides):
    fields = dict(
        id=2,
        name="Bob",
        email="bob@example.com",
        phone="555-0199",
    )
    fields.update(overrides)
    return Customer(**fields)


class PaymentCharacterizationTests(TestCase):
    def setUp(self):
        self.processor = PaymentProcessor()

    def test_credit_card_returns_exact_string_and_prints_charging_line(self):
        order = Order(
            id=1,
            customer=make_vip(),
            payment_method="credit_card",
            items=[OrderItem(1, "Laptop", 999.99, 1)],
        )
        receipt, output = capture_stdout(self.processor.process, order, 819.99)
        self.assertEqual(receipt, "paid_by_credit_card:819.99")
        self.assertEqual(
            output,
            "[payment] Charging card 4111 1111 1111 1111 819.99\n",
        )

    def test_paypal_returns_exact_string_and_prints_charging_line(self):
        order = Order(
            id=2,
            customer=make_regular(),
            payment_method="paypal",
            items=[OrderItem(3, "Clean Code", 45.00, 2)],
        )
        receipt, output = capture_stdout(self.processor.process, order, 7.00)
        self.assertEqual(receipt, "paid_by_paypal:7.00")
        self.assertEqual(
            output,
            "[payment] Charging PayPal bob@example.com 7.00\n",
        )

    def test_bitcoin_returns_exact_string_and_prints_charging_line(self):
        order = Order(
            id=3,
            customer=make_regular(bitcoin_address="1AbcDef"),
            payment_method="bitcoin",
            items=[OrderItem(4, "Widget", 3.25, 1)],
        )
        receipt, output = capture_stdout(self.processor.process, order, 3.25)
        self.assertEqual(receipt, "paid_by_bitcoin:3.25")
        self.assertEqual(
            output,
            "[payment] Charging BTC 1AbcDef 3.25\n",
        )

    def test_unknown_payment_method_raises_exact_value_error(self):
        order = Order(
            id=4,
            customer=make_regular(),
            payment_method="cash",
            items=[OrderItem(5, "Thing", 1.00, 1)],
        )
        with self.assertRaises(ValueError) as ctx:
            capture_stdout(self.processor.process, order, 1.00)
        self.assertEqual(str(ctx.exception), "Unknown payment method: 'cash'")


class DiscountCharacterizationTests(TestCase):
    def setUp(self):
        self.calculator = DiscountCalculator()

    def calculate_for(self, customer, items=None, coupons=None):
        order = Order(
            id=100,
            customer=customer,
            items=list(items or []),
            coupons=list(coupons or []),
        )
        return self.calculator.calculate(order)

    def test_vip_takes_twenty_percent_even_with_quantity_and_coupon(self):
        items = [OrderItem(1, "Bulk", 10.00, 10)]
        self.assertEqual(self.calculate_for(make_vip(), items, ["WELCOME10"]), 20.0)

    def test_quantity_takes_ten_percent_for_non_vip(self):
        items = [OrderItem(1, "Bulk", 10.00, 10)]
        self.assertEqual(self.calculate_for(make_regular(), items), 10.0)

    def test_quantity_rule_wins_over_coupon(self):
        items = [OrderItem(1, "Bulk", 10.00, 10)]
        self.assertEqual(
            self.calculate_for(make_regular(), items, ["WELCOME10"]),
            10.0,
        )

    def test_coupon_takes_ten_percent_when_no_other_rule_matches(self):
        items = [OrderItem(1, "Book", 33.33, 1)]
        self.assertEqual(
            self.calculate_for(make_regular(), items, ["WELCOME10"]),
            3.33,
        )

    def test_no_matching_rule_yields_zero_discount(self):
        items = [OrderItem(1, "Book", 50.00, 1)]
        self.assertEqual(self.calculate_for(make_regular(), items), 0.0)

    def test_quantity_rule_needs_ten_items(self):
        items = [OrderItem(1, "Bulk", 10.00, 9)]
        self.assertEqual(self.calculate_for(make_regular(), items), 0.0)

    def test_discount_is_rounded_to_two_decimals_upward(self):
        items = [OrderItem(1, "Gadget", 19.99, 1)]
        self.assertEqual(self.calculate_for(make_vip(), items), 4.0)


class ValidationCharacterizationTests(TestCase):
    def setUp(self):
        self.service = OrderService()

    def test_empty_non_bundle_order_is_rejected_before_pricing(self):
        order = Order(id=10, customer=make_regular())
        with self.assertRaises(ValueError) as ctx:
            self.service.process_order(order)
        self.assertEqual(str(ctx.exception), "Order has no items")

    def test_missing_payment_method_is_rejected_after_item_check(self):
        order = Order(
            id=11,
            customer=make_regular(),
            items=[OrderItem(1, "Book", 10.00, 1)],
        )
        with self.assertRaises(ValueError) as ctx:
            self.service.process_order(order)
        self.assertEqual(str(ctx.exception), "Order has no payment method")


class DemoStdoutCharacterizationTests(TestCase):
    EXPECTED_DEMO_OUTPUT = (
        ">>> Checkout a simple order\n"
        "[payment] Charging card 4111 1111 1111 1111 819.99\n"
        "[email] to alice@example.com: Order 101 total $819.99"
        " (paid_by_credit_card:819.99)\n"
        "[sms] to 555-0100: Order 101 total $819.99"
        " (paid_by_credit_card:819.99)\n"
        "--- Receipt for order 101 ---\n"
        "  Laptop               x1  $999.99\n"
        "  Mouse                x1  $25.00\n"
        "  Subtotal    $1024.99\n"
        "  Discount   -$205.00\n"
        "  Shipping    $0.00\n"
        "  TOTAL       $819.99\n"
        "  Payment     paid_by_credit_card:819.99\n"
        "\n"
        ">>> Checkout a bundle of two orders\n"
        "[payment] Charging card 4111 1111 1111 1111 5.00\n"
        "[email] to alice@example.com: Order 103 total $5.00"
        " (paid_by_credit_card:5.00)\n"
        "[sms] to 555-0100: Order 103 total $5.00"
        " (paid_by_credit_card:5.00)\n"
        "--- Receipt for order 103 ---\n"
        "  Subtotal    $0.00\n"
        "  Discount   -$0.00\n"
        "  Shipping    $5.00\n"
        "  TOTAL       $5.00\n"
        "  Payment     paid_by_credit_card:5.00\n"
    )

    def test_full_demo_output_matches_baseline_exactly(self):
        _, output = capture_stdout(main)
        self.assertEqual(output, self.EXPECTED_DEMO_OUTPUT)


class CheckoutFlowCharacterizationTests(TestCase):
    def test_simple_checkout_pins_status_persistence_and_output_order(self):
        service = OrderService()
        order = Order(
            id=201,
            customer=make_regular(),
            payment_method="paypal",
            coupons=["WELCOME10"],
            items=[OrderItem(6, "Gadget", 30.00, 2)],
        )

        returned, output = capture_stdout(service.process_order, order)

        self.assertIs(returned, order)
        self.assertEqual(order.status, "paid")
        self.assertIs(service.database.load_order(201), order)
        self.assertEqual(
            output,
            "[payment] Charging PayPal bob@example.com 59.00\n"
            "[email] to bob@example.com: Order 201 total $59.00"
            " (paid_by_paypal:59.00)\n"
            "[sms] to 555-0199: Order 201 total $59.00"
            " (paid_by_paypal:59.00)\n"
            "--- Receipt for order 201 ---\n"
            "  Gadget               x2  $60.00\n"
            "  Subtotal    $60.00\n"
            "  Discount   -$6.00\n"
            "  Shipping    $5.00\n"
            "  TOTAL       $59.00\n"
            "  Payment     paid_by_paypal:59.00\n",
        )

    def test_notify_false_suppresses_email_and_sms_but_keeps_receipt(self):
        service = OrderService()
        order = Order(
            id=202,
            customer=make_regular(),
            payment_method="paypal",
            items=[OrderItem(7, "Mug", 200.00, 1)],
        )

        _, output = capture_stdout(service.process_order, order, notify=False)

        self.assertNotIn("[email]", output)
        self.assertNotIn("[sms]", output)
        self.assertIn("[payment] Charging PayPal bob@example.com 200.00", output)
        self.assertIn("--- Receipt for order 202 ---", output)

    def test_bundle_checkout_keeps_zero_subtotal_and_five_dollar_total(self):
        service = OrderService()
        laptop, books, bundle = build_demo_orders()
        self.assertIsNone(service.database.load_order(bundle.id))

        returned, output = capture_stdout(service.process_order, bundle)

        self.assertIs(returned, bundle)
        self.assertEqual(bundle.status, "paid")
        self.assertIs(service.database.load_order(103), bundle)
        self.assertIn("[payment] Charging card 4111 1111 1111 1111 5.00", output)
        self.assertIn("  Subtotal    $0.00", output)
        self.assertIn("  Discount   -$0.00", output)
        self.assertIn("  Shipping    $5.00", output)
        self.assertIn("  TOTAL       $5.00", output)
        self.assertIn("  Payment     paid_by_credit_card:5.00", output)


class StorageCharacterizationTests(TestCase):
    def test_save_then_load_roundtrips_same_instance(self):
        database = MySqlDatabase()
        order = Order(id=300, customer=make_regular())

        database.save_order(order)

        self.assertIs(database.load_order(300), order)

    def test_load_unknown_id_returns_none(self):
        database = MySqlDatabase()
        self.assertIsNone(database.load_order(999))


class NotificationCharacterizationTests(TestCase):
    def test_notification_service_prints_email_sms_and_push_lines(self):
        notifier = NotificationService()

        _, output = capture_stdout(
            lambda: (
                notifier.send_email(make_regular(), "hello-e"),
                notifier.send_sms(make_regular(), "hello-s"),
                notifier.send_push(make_regular(), "hello-p"),
            )
        )

        self.assertEqual(
            output,
            "[email] to bob@example.com: hello-e\n"
            "[sms] to 555-0199: hello-s\n"
            "[push] to Bob: hello-p\n",
        )

    def test_sms_only_notifier_sends_sms_successfully(self):
        notifier = SmsOnlyNotifier()

        _, output = capture_stdout(notifier.send_sms, make_regular(), "sms-ok")

        self.assertEqual(output, "[sms] to 555-0199: sms-ok\n")

    def test_sms_only_notifier_email_raises_not_implemented(self):
        notifier = SmsOnlyNotifier()
        with self.assertRaises(NotImplementedError) as ctx:
            notifier.send_email(make_regular(), "nope")
        self.assertEqual(str(ctx.exception), "An SMS notifier cannot send email")

    def test_sms_only_notifier_push_raises_not_implemented(self):
        notifier = SmsOnlyNotifier()
        with self.assertRaises(NotImplementedError) as ctx:
            notifier.send_push(make_regular(), "nope")
        self.assertEqual(str(ctx.exception), "An SMS notifier cannot send push")


class BundleZeroValueCharacterizationTests(TestCase):
    def setUp(self):
        self.laptop, self.books, self.bundle = build_demo_orders()

    def test_bundle_is_currently_a_subclass_of_order(self):
        self.assertIsInstance(self.bundle, Order)

    def test_bundle_reports_inherited_zero_values_despite_children(self):
        self.assertEqual(self.bundle.items, [])
        self.assertEqual(self.bundle.subtotal, 0)
        self.assertEqual(self.bundle.item_count, 0)
        self.assertEqual(self.bundle.status, "pending")

    def test_bundle_children_keep_their_own_totals(self):
        self.assertEqual(self.laptop.subtotal, 1024.99)
        self.assertEqual(self.books.subtotal, 170.0)
        child_total = sum(child.subtotal for child in self.bundle.orders)
        self.assertEqual(child_total, 1194.99)
