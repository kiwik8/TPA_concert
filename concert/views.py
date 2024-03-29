import os
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.mail.message import EmailMessage
from django.core.mail import get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from concert.models import Price, Client, Question, Product
from django.shortcuts import redirect
from django.urls import resolve
from django.templatetags.static import static
from django.contrib.staticfiles import finders
import stripe
# Create your views here.




stripe.api_key = settings.STRIPE_SECRET_KEY



def pdf_view(request):
    # file_path = finders.find('concert/documents/tpa-ecrit.pdf')
    url = "https://cdn.jsdelivr.net/gh/kiwik8/TPA_concert/static/concert/documents/tpa-ecrit.pdf"
    return redirect(url)
    #response = FileResponse(open(url, 'rb'), content_type='application/pdf')
    #return response

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        quantity = int(request.POST.get('quantity'))
        price = request.POST.get('price')
        price = Price.objects.get(price=price)
        product = price.product
        if product.stock <=0:
            return render(request, 'concert/cancel.html', {"message" : "Plus de place disponible"}, status=201)
        checkout_session = stripe.checkout.Session.create(
            metadata={
                'product_id': product.id,
                'quantity': quantity,
            },
            payment_method_types=['card', 'bancontact'],
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
        message = "Paiement effectué avec succès"
        try:
            if context['message'] is None:
                context['paid'] = True
                context['message'] = message
            else:
                context['paid'] = False
            return context
        except KeyError:
            context['paid'] = True
            context['message'] = message
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
                payload, sig_header, settings.STRIPE_WEBHOOK
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
            customer_name = session["customer_details"]["name"]
            payment_intent = session["payment_intent"]
            product = session["metadata"]["product_id"]
            quantity = session["metadata"]["quantity"]
            quantity = int(quantity)
            product = Product.objects.get(id=product)
            product.stock -= quantity
            p = Product.objects.get(name="Pack Ticket+CD")
            if p == product:
                cd = Product.objects.get(name="CD")
                ticket = Product.objects.get(name="Ticket")
                ticket.stock -= quantity
                cd.stock -= quantity
                ticket.save()
                cd.save()
            product.save()
            Client.objects.create(name=customer_name, email=customer_email, product=product, quantity=quantity)

            # Send an email to the customer with the order details
            html_message = render_to_string('concert/mail.html', {'name': customer_name})
            message = strip_tags(html_message)

            ### EMail part 
            email = EmailMessage()
            email.subject = "Reçu de commande"
            email.body = message
            email.to = [customer_email]
            email.from_email = "support@bea7s.store"

            # email.attach_file('static/concert/concert.ics', 'text/calendar')
            email.send()


        return HttpResponse(status=200)
    except KeyError as e:
        return HttpResponse(status=405)



def redirect_to(request):
    try:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Question.objects.create(fisrt_name=first_name, last_name=last_name, email=email, message=message)
        return render(request, 'concert/success.html', {'message': "Question envoyée"})
    except:
        return render(request, 'concert/cancel.html', {'message': "Erreur, contactez l'admin : Martin Gouverneur"})

def mail_view(request):
    return render(request, 'concert/mail.html')

def download(request):
    file_path = static("concert/medias/story.mp4")
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="video/mp4")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response

def index(request):
    if request.method == "POST":
        return redirect_to(request)
    return render(request, 'concert/index.html')


def buy(request):
    return render(request, 'concert/buy.html')
