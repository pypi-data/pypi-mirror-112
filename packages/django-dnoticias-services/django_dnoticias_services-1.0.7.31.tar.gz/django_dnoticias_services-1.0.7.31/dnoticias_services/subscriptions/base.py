from django.conf import settings


class BaseSubscriptionRequest:
    def __init__(self):
        self.api_key = getattr(settings, "SUBSCRIPTION_SERVICE_ACCOUNT_API_KEY", None)
        self.timeout = getattr(settings, "SUBSCRIPTION_SERVICE_REQUEST_TIMEOUT", 5)
