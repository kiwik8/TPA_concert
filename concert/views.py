from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from concert.models import EmailClient, Price
from django.shortcuts import redirect
import stripe
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    return render(request, 'concert/index.html')


@csrf_protect
def suscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        EmailClient.objects.create(email=email)
    context = {
        "email": email
    }
    return render(request, 'concert/suscribed.html', context)

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            email = request.POST.get('stripeToken')
        price = Price.objects.get(id=1)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=settings.BASE_URL + '/success',
            cancel_url=settings.BASE_URL + '/cancel',
        )
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "concert/success.html"


class CancelView(TemplateView):
    template_name = "concert/cancel.html"

