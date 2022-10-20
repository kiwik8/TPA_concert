from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from concert.models import Newsletter, Price, Client
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
        Newsletter.objects.create(email=email)
    context = {
        "email": email
    }
    return render(request, 'concert/suscribed.html', context)

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
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

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        payment_intent = session["payment_intent"]

        Client.objects.create(email=customer_email)

        send_mail("Test order", "J'adore la beuh", settings.EMAIL_HOST_USER, [customer_email])

    return HttpResponse(status=200)