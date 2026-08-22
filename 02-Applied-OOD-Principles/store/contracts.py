from typing import Protocol, runtime_checkable

from store.models import CheckoutOrder, Customer


@runtime_checkable
class DiscountCalculatorPort(Protocol):
    def calculate(self, order: CheckoutOrder) -> float: ...


@runtime_checkable
class ShippingCalculatorPort(Protocol):
    def calculate(self, subtotal: float) -> float: ...


@runtime_checkable
class PaymentProcessorPort(Protocol):
    def process(self, order: CheckoutOrder, amount: float) -> str: ...


@runtime_checkable
class EmailSender(Protocol):
    def send_email(self, customer: Customer, message: str) -> None: ...


@runtime_checkable
class SmsSender(Protocol):
    def send_sms(self, customer: Customer, message: str) -> None: ...


@runtime_checkable
class OrderRepository(Protocol):
    def save_order(self, order: CheckoutOrder) -> None: ...


@runtime_checkable
class ReceiptPresenter(Protocol):
    def print_receipt(
        self,
        order: CheckoutOrder,
        subtotal: float,
        discount: float,
        shipping: float,
        total: float,
        receipt: str,
    ) -> None: ...
