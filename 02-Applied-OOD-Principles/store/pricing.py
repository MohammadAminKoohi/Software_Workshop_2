from typing import Protocol, Sequence

from store.models import CheckoutOrder


class ShippingCalculator:
    def calculate(self, subtotal: float) -> float:
        return 5.0 if subtotal < 100 else 0.0


class DiscountRule(Protocol):
    def discount_for(self, order: CheckoutOrder) -> float | None: ...


class VipDiscountRule:
    def discount_for(self, order: CheckoutOrder) -> float | None:
        if order.customer.is_vip:
            return order.subtotal * 0.20
        return None


class QuantityDiscountRule:
    def discount_for(self, order: CheckoutOrder) -> float | None:
        if order.item_count >= 10:
            return order.subtotal * 0.10
        return None


class WelcomeCouponDiscountRule:
    def discount_for(self, order: CheckoutOrder) -> float | None:
        if "WELCOME10" in order.coupons:
            return order.subtotal * 0.10
        return None


class DiscountCalculator:
    def __init__(self, rules: Sequence[DiscountRule]):
        self.rules = tuple(rules)

    def calculate(self, order: CheckoutOrder) -> float:
        for rule in self.rules:
            discount = rule.discount_for(order)
            if discount is not None:
                return round(discount, 2)
        return 0.0
