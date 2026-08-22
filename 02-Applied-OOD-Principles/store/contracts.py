from typing import Protocol, runtime_checkable

from store.models import Customer, Order


@runtime_checkable
class DiscountCalculatorPort(Protocol):
    def calculate(self, order: Order) -> float: ...


@runtime_checkable
class PaymentProcessorPort(Protocol):
    def process(self, order: Order, amount: float) -> str: ...


@runtime_checkable
class EmailSender(Protocol):
    def send_email(self, customer: Customer, message: str) -> None: ...


@runtime_checkable
class SmsSender(Protocol):
    def send_sms(self, customer: Customer, message: str) -> None: ...


@runtime_checkable
class OrderRepository(Protocol):
    def save_order(self, order: Order) -> None: ...
