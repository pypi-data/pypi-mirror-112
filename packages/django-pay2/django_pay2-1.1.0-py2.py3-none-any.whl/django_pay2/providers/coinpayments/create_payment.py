from django_pay2.decorators import handle_debug
from django_pay2.models import Payment

from .api import get_api


@handle_debug
def create_coinpayments_payment(request, amount, desc, receiver, buyer_email, currency):
    payment = Payment.objects.create(amount=amount, receiver=receiver)
    api = get_api()
    return api.generate_payment_method(
        request, amount, currency, payment.id, buyer_email
    )
