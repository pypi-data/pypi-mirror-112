from django_pay2.decorators import handle_form_debug
from django_pay2.models import Payment

from .api import get_api


@handle_form_debug
def create_perfect_money_payment(request, amount, desc, receiver, currency):
    payment = Payment.objects.create(amount=amount, receiver=receiver)
    api = get_api()
    return api.generate_payment_method(request, amount, currency, payment.id)
