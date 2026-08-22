from store.contracts import (
    DiscountCalculatorPort,
    EmailSender,
    OrderRepository,
    PaymentProcessorPort,
    SmsSender,
)
from store.models import BundleOrder, Order


class OrderService:
    def __init__(
        self,
        discount_calculator: DiscountCalculatorPort,
        payment_processor: PaymentProcessorPort,
        email_sender: EmailSender,
        sms_sender: SmsSender,
        database: OrderRepository,
    ):
        self.discount_calculator = discount_calculator
        self.payment_processor = payment_processor
        self.email_sender = email_sender
        self.sms_sender = sms_sender
        self.database = database

    def process_order(self, order: Order, notify: bool = True) -> Order:
        # 1. validate
        if not order.items and not isinstance(order, BundleOrder):
            raise ValueError("Order has no items")
        if not order.payment_method:
            raise ValueError("Order has no payment method")

        # 2. price it
        subtotal = order.subtotal
        discount = self.discount_calculator.calculate(order)
        shipping = 5.0 if subtotal < 100 else 0.0
        total = round(subtotal - discount + shipping, 2)

        # 3. charge the customer
        receipt = self.payment_processor.process(order, total)

        # 4. persist
        order.status = "paid"
        self.database.save_order(order)

        # 5. notify
        if notify:
            message = f"Order {order.id} total ${total:.2f} ({receipt})"
            self.email_sender.send_email(order.customer, message)
            self.sms_sender.send_sms(order.customer, message)

        # 6. print a receipt
        self._print_receipt(order, subtotal, discount, shipping, total, receipt)
        return order

    def _print_receipt(self, order, subtotal, discount, shipping, total, receipt):
        print(f"--- Receipt for order {order.id} ---")
        for item in order.items:
            print(f"  {item.name:20s} x{item.quantity}  ${item.line_total:.2f}")
        print(f"  Subtotal    ${subtotal:.2f}")
        print(f"  Discount   -${discount:.2f}")
        print(f"  Shipping    ${shipping:.2f}")
        print(f"  TOTAL       ${total:.2f}")
        print(f"  Payment     {receipt}")
