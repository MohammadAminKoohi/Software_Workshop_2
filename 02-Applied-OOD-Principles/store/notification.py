class NotificationService:
    def send_email(self, customer, message: str) -> None:
        print(f"[email] to {customer.email}: {message}")

    def send_sms(self, customer, message: str) -> None:
        print(f"[sms] to {customer.phone}: {message}")

    def send_push(self, customer, message: str) -> None:
        print(f"[push] to {customer.name}: {message}")


class SmsOnlyNotifier:
    def send_sms(self, customer, message: str) -> None:
        print(f"[sms] to {customer.phone}: {message}")
