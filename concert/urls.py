from django.contrib import admin
from django.urls import path, include
import concert.views
from concert.views import CreateCheckoutSessionView, CancelView, SuccessView, stripe_webhook

urlpatterns = [
    path('homepage/', concert.views.homepage, name='homepage'),
    path('', concert.views.redirect_to),
    path('home', concert.views.redirect_to),
    path('suscribe', concert.views.suscribe, name="suscribe"),
    path('cancel', CancelView.as_view(), name="cancel"),
    path('success', SuccessView.as_view(), name="success"),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]