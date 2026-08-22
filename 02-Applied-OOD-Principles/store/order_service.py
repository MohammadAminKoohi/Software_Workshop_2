from store.contracts import (
    DiscountCalculatorPort,
    EmailSender,
    OrderRepository,
    PaymentProcessorPort,
    ReceiptPresenter,
    ShippingCalculatorPort,
    SmsSender,
)
from store.models import BundleOrder, CheckoutOrder


class OrderService:
    def __init__(
        self,
        discount_calculator: DiscountCalculatorPort,
        shipping_calculator: ShippingCalculatorPort,
        payment_processor: PaymentProcessorPort,
        email_sender: EmailSender,
        sms_sender: SmsSender,
        database: OrderRepository,
        receipt_printer: ReceiptPresenter,
    ):
        self.discount_calculator = discount_calculator
        self.shipping_calculator = shipping_calculator
        self.payment_processor = payment_processor
        self.email_sender = email_sender
        self.sms_sender = sms_sender
        self.database = database
        self.receipt_printer = receipt_printer

    def process_order(
        self, order: CheckoutOrder, notify: bool = True
    ) -> CheckoutOrder:
        # 1. validate
        if not order.items and not isinstance(order, BundleOrder):
            raise ValueError("Order has no items")
        if not order.payment_method:
            raise ValueError("Order has no payment method")

        # 2. price it
        subtotal = order.subtotal
        discount = self.discount_calculator.calculate(order)
        shipping = self.shipping_calculator.calculate(subtotal)
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
        self.receipt_printer.print_receipt(
            order, subtotal, discount, shipping, total, receipt
        )
        return order
