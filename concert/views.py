from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from concert.models import Price, Client, Question
from django.shortcuts import redirect
from django.urls import resolve
import stripe
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY




@csrf_protect
def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        Client.objects.create(email=email)
        return render(request, 'concert/success.html', {"message": "Merci pour votre inscription à la newsletter"})
    else:
        return render(request, 'concert/cancel.html', {"message" : "INVALID METHOD"})

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        quantity = int(request.POST.get('quantity'))
        price = Price.objects.order_by("id").first()
        product = price.product
        product.stock -= quantity
        product.save()
        success = reverse('success')
        cancel = reverse('cancel')
        if product.stock <=0:
            return render(request, 'concert/cancel.html', {"message" : "Plus de place disponible"}, status=201)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': quantity,
                },
            ],
            mode='payment',
            success_url= settings.BASE_URL + '/success',
            cancel_url=settings.BASE_URL + '/cancel',
        )
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "concert/success.html"
    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        context['message'] = "Paiement effectué avec succès"
        return context


class CancelView(TemplateView):
    template_name = "concert/cancel.html"
    def get_context_data(self, **kwargs):
        context = super(CancelView, self).get_context_data(**kwargs)
        context['message'] = "Paiement annulé"
        return context

@csrf_exempt
def stripe_webhook(request):
    try:
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
            #url = request.build_absolute_uri('/view_mail/')
            #pdf = weasyprint.HTML(url=url).write_pdf()
            open('ticket.pdf', 'wb').write(pdf)
            subject = 'Ticket de réservation pour le concert de BEA7S'
            html_message = render_to_string('concert/mail.html')
            plain_message = strip_tags(html_message)
            from_email = 'From <martingouv2005@hotmail.com>'
            to = customer_email
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            #send_mail("Ticket de réservation pour le concert de BEA7S", "Facture", settings.EMAIL_HOST_USER, [customer_email])

        return HttpResponse(status=200)
    except KeyError as e:
        return HttpResponse(status=405)

def homepage(request):
    if 'redirected' in request.COOKIES:
        response = render(request, 'concert/homepage.html')
        response.delete_cookie('redirected')
        return response
    else:
        return redirect_to(request)


def redirect_to(request):
    if request.POST:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Question.objects.create(fisrt_name=first_name, last_name=last_name, email=email, message=message)
        return render(request, 'concert/success.html', {'message': "Question envoyée"})
    if 'redirected' in request.COOKIES:
        return render(request, 'concert/index.html')
    else:
        response = render(request, 'concert/homepage.html')
        response.set_cookie('redirected', 'true', max_age=60*2)
        return response

def mail_view(request):
    return render(request, 'concert/mail.html')

