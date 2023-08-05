from django_pay2.decorators import handle_debug
from django_pay2.models import Payment
from datetime import timedelta

from .api import get_api


@handle_debug
def create_qiwi_payment(request, amount, desc, receiver, currency, expirate_at=None):
    payment = Payment.objects.create(amount=amount, receiver=receiver)
    expirate_at = expirate_at or payment.created + timedelta(days=1)
    api = get_api()
    return api.generate_payment_method(amount, currency, expirate_at, payment.id)
