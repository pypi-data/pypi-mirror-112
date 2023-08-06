from django.conf import settings
from .base import BasePaymentRequest


class GetStripeSubscription(BasePaymentRequest):
    def __call__(self, remote_subscription_id, api_key=None, timeout=None):
        self.set_api_url(
            settings.PAYMENTS_GET_STRIPE_SUBSCRIPTION_API_URL,
            (remote_subscription_id, )
        )
        return self.get({}, api_key, timeout)


get_stripe_subscription = GetStripeSubscription()

__all__ = ('get_stripe_subscription', )
