from unittest import TestCase

from store.main import build_discount_rules
from store.models import Order, OrderItem
from store.pricing import DiscountCalculator

from test_characterization import make_regular, make_vip


def order_for(customer, quantity=1, price=100.0, coupons=None):
    return Order(
        id=801,
        customer=customer,
        items=[OrderItem(1, "Item", price, quantity)],
        coupons=list(coupons or []),
    )


class ExistingDiscountRuleTests(TestCase):
    def setUp(self):
        self.calculator = DiscountCalculator(build_discount_rules())

    def test_vip_rule_preserves_twenty_percent(self):
        self.assertEqual(self.calculator.calculate(order_for(make_vip())), 20.0)

    def test_quantity_rule_preserves_ten_percent(self):
        order = order_for(make_regular(), quantity=10, price=10.0)
        self.assertEqual(self.calculator.calculate(order), 10.0)

    def test_coupon_rule_preserves_ten_percent(self):
        order = order_for(make_regular(), price=33.33, coupons=["WELCOME10"])
        self.assertEqual(self.calculator.calculate(order), 3.33)

    def test_no_rule_preserves_zero_discount(self):
        self.assertEqual(self.calculator.calculate(order_for(make_regular())), 0.0)

    def test_rule_order_preserves_vip_quantity_coupon_precedence(self):
        order = order_for(
            make_vip(), quantity=10, price=10.0, coupons=["WELCOME10"]
        )
        self.assertEqual(self.calculator.calculate(order), 20.0)

    def test_quantity_still_precedes_coupon(self):
        order = order_for(
            make_regular(), quantity=10, price=10.0, coupons=["WELCOME10"]
        )
        self.assertEqual(self.calculator.calculate(order), 10.0)


class DiscountExtensionBoundaryTests(TestCase):
    def test_synthetic_rule_extends_calculator_without_algorithm_change(self):
        calls = []

        class TestOnlyRule:
            def discount_for(self, order):
                calls.append(order)
                return 12.345

        order = order_for(make_regular())
        calculator = DiscountCalculator([TestOnlyRule()])

        self.assertEqual(calculator.calculate(order), 12.35)
        self.assertEqual(calls, [order])

    def test_calculator_requires_rules_and_copies_the_sequence(self):
        with self.assertRaises(TypeError):
            DiscountCalculator()

        rules = []
        calculator = DiscountCalculator(rules)
        rules.append(object())

        self.assertEqual(calculator.calculate(order_for(make_regular())), 0.0)
