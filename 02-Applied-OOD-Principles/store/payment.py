from typing import Mapping, Protocol

from store.models import Order


class PaymentHandler(Protocol):
    def process(self, order: Order, amount: float) -> str: ...


class CreditCardPaymentHandler:
    def process(self, order: Order, amount: float) -> str:
        card = order.customer.credit_card
        print(f"[payment] Charging card {card} {amount:.2f}")
        return f"paid_by_credit_card:{amount:.2f}"


class PaypalPaymentHandler:
    def process(self, order: Order, amount: float) -> str:
        email = order.customer.email
        print(f"[payment] Charging PayPal {email} {amount:.2f}")
        return f"paid_by_paypal:{amount:.2f}"


class BitcoinPaymentHandler:
    def process(self, order: Order, amount: float) -> str:
        address = order.customer.bitcoin_address
        print(f"[payment] Charging BTC {address} {amount:.2f}")
        return f"paid_by_bitcoin:{amount:.2f}"


class PaymentProcessor:
    def __init__(self, handlers: Mapping[str, PaymentHandler]):
        self.handlers = dict(handlers)

    def process(self, order: Order, amount: float) -> str:
        method = order.payment_method
        handler = self.handlers.get(method)
        if handler is None:
            raise ValueError(f"Unknown payment method: {method!r}")
        return handler.process(order, amount)
