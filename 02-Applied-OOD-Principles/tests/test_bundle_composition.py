from unittest import TestCase

from store.main import build_demo_orders
from store.models import BundleOrder, Order

from test_characterization import capture_stdout, make_default_service, make_regular


class BundleCompositionModelTests(TestCase):
    def setUp(self):
        self.laptop, self.books, self.bundle = build_demo_orders()

    def test_bundle_contains_orders_without_being_an_order(self):
        self.assertIsInstance(self.bundle, BundleOrder)
        self.assertNotIsInstance(self.bundle, Order)
        self.assertEqual(self.bundle.orders, [self.laptop, self.books])

    def test_baseline_compatible_fields_and_zero_values_are_preserved(self):
        self.assertEqual(self.bundle.id, 103)
        self.assertEqual(self.bundle.items, [])
        self.assertEqual(self.bundle.coupons, [])
        self.assertEqual(self.bundle.status, "pending")
        self.assertEqual(self.bundle.payment_method, "credit_card")
        self.assertEqual(self.bundle.subtotal, 0.0)
        self.assertEqual(self.bundle.item_count, 0)

    def test_child_values_remain_independent_and_are_not_aggregated(self):
        self.assertEqual(self.laptop.subtotal, 1024.99)
        self.assertEqual(self.books.subtotal, 170.0)
        self.assertEqual(sum(order.subtotal for order in self.bundle.orders), 1194.99)
        self.assertEqual(self.bundle.subtotal, 0.0)

    def test_mutable_defaults_are_not_shared_between_bundles(self):
        first = BundleOrder(id=1, customer=make_regular(), orders=[])
        second = BundleOrder(id=2, customer=make_regular(), orders=[])
        first.items.append(object())
        first.coupons.append("TEST")

        self.assertEqual(second.items, [])
        self.assertEqual(second.coupons, [])


class BundleCompositionCheckoutTests(TestCase):
    def test_bundle_checkout_preserves_total_status_persistence_and_receipt(self):
        service = make_default_service()
        _, _, bundle = build_demo_orders()

        returned, output = capture_stdout(service.process_order, bundle)

        self.assertIs(returned, bundle)
        self.assertEqual(bundle.status, "paid")
        self.assertIs(service.database.load_order(bundle.id), bundle)
        self.assertIn("[payment] Charging card 4111 1111 1111 1111 5.00", output)
        self.assertIn("  Subtotal    $0.00", output)
        self.assertIn("  Shipping    $5.00", output)
        self.assertIn("  TOTAL       $5.00", output)
        self.assertIn("  Payment     paid_by_credit_card:5.00", output)

    def test_bundle_still_bypasses_the_empty_item_validation_branch(self):
        service = make_default_service()
        bundle = BundleOrder(id=3, customer=make_regular(), orders=[])
        bundle.payment_method = "paypal"

        returned, output = capture_stdout(service.process_order, bundle)

        self.assertIs(returned, bundle)
        self.assertIn("  TOTAL       $5.00", output)
