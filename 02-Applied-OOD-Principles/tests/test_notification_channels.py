from unittest import TestCase

from store.models import Order, OrderItem
from store.notification import NotificationService, SmsOnlyNotifier
from store.order_service import OrderService

from test_characterization import capture_stdout, make_regular
from test_dependency_injection import make_fakes


class SmsOnlyContractTests(TestCase):
    def test_sms_only_notifier_is_not_a_notification_service_subclass(self):
        self.assertFalse(issubclass(SmsOnlyNotifier, NotificationService))

    def test_sms_only_notifier_exposes_only_supported_channel(self):
        notifier = SmsOnlyNotifier()
        self.assertTrue(callable(notifier.send_sms))
        self.assertFalse(hasattr(notifier, "send_email"))
        self.assertFalse(hasattr(notifier, "send_push"))

    def test_sms_output_is_preserved(self):
        _, output = capture_stdout(
            SmsOnlyNotifier().send_sms, make_regular(), "channel message"
        )
        self.assertEqual(output, "[sms] to 555-0199: channel message\n")


class NarrowChannelInjectionTests(TestCase):
    def test_checkout_uses_email_and_sms_substitutes_independently(self):
        fakes = make_fakes()
        service = OrderService(**fakes)
        order = Order(
            id=901,
            customer=make_regular(),
            payment_method="paypal",
            items=[OrderItem(1, "Item", 100.0, 1)],
        )

        service.process_order(order)

        self.assertEqual(len(fakes["email_sender"].calls), 1)
        self.assertEqual(len(fakes["sms_sender"].calls), 1)
        self.assertIsNot(fakes["email_sender"], fakes["sms_sender"])

    def test_notify_false_skips_both_narrow_channels(self):
        fakes = make_fakes()
        service = OrderService(**fakes)
        order = Order(
            id=902,
            customer=make_regular(),
            payment_method="paypal",
            items=[OrderItem(1, "Item", 100.0, 1)],
        )

        service.process_order(order, notify=False)

        self.assertEqual(fakes["email_sender"].calls, [])
        self.assertEqual(fakes["sms_sender"].calls, [])
