from store.models import BundleOrder, Customer, Order, OrderItem
from store.notification import NotificationService
from store.order_service import OrderService
from store.payment import PaymentProcessor
from store.pricing import DiscountCalculator, ShippingCalculator
from store.storage import MySqlDatabase


def build_demo_orders():
    vip = Customer(
        id=1, name="Alice", email="alice@example.com",
        phone="555-0100", is_vip=True, credit_card="4111 1111 1111 1111",
    )
    regular = Customer(
        id=2, name="Bob", email="bob@example.com", phone="555-0199",
    )

    laptop = Order(
        id=101, customer=vip, payment_method="credit_card",
        items=[OrderItem(1, "Laptop", 999.99, 1),
               OrderItem(2, "Mouse", 25.00, 1)],
    )

    books = Order(
        id=102, customer=regular, payment_method="paypal",
        items=[OrderItem(3, "Clean Code", 45.00, 2),
               OrderItem(4, "Pragmatic Programmer", 40.00, 2)],
    )

    bundle = BundleOrder(id=103, customer=vip, orders=[laptop, books])
    bundle.payment_method = "credit_card"
    return laptop, books, bundle


def build_demo_service() -> OrderService:
    notification = NotificationService()
    return OrderService(
        discount_calculator=DiscountCalculator(),
        shipping_calculator=ShippingCalculator(),
        payment_processor=PaymentProcessor(),
        email_sender=notification,
        sms_sender=notification,
        database=MySqlDatabase(),
    )


def main() -> None:
    service = build_demo_service()
    laptop, books, bundle = build_demo_orders()

    print(">>> Checkout a simple order")
    service.process_order(laptop)

    print("\n>>> Checkout a bundle of two orders")
    service.process_order(bundle)


if __name__ == "__main__":
    main()
