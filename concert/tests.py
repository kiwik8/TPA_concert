from django.test import TestCase
from django.urls import resolve, reverse
import os
import logging
from .views import *
from .models import *
from django.conf import settings
# Create your tests here.

logger = logging.getLogger("Logs")

class TestUrls(TestCase):

    def setUp(self):
        self.stripe_product_id = os.environ.get("STRIPE_PRODUCT_ID")
        self.stripe_price_id = os.environ.get("STRIPE_PRICE_ID")
        self.product = Product.objects.create(name="Ticket", stripe_product_id=self.stripe_product_id, stock=50)
        self.price = Price.objects.create(product=self.product, stripe_price_id=self.stripe_price_id, price=10)

    def test_index_url(self):
        url = reverse('index')
        response = self.client.get(url)
        status_code = response.status_code
        self.assertEquals(resolve(url).func, index)
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, "concert/index.html")
    def test_get_create_checkout_session_url(self):
        url = reverse("checkout")
        response = self.client.get(url)
        status_code = response.status_code
        self.assertEquals(resolve(url).func.view_class, CreateCheckoutSessionView)
        self.assertEqual(status_code, 405)
    def test_post_create_checkout_session_url(self):
        url = reverse("checkout")
        context = {"quantity": 1, "price": self.price.price}
        response = self.client.post(url, context)
        status_code = response.status_code
        self.assertEquals(resolve(url).func.view_class, CreateCheckoutSessionView)
        self.assertEqual(status_code, 302)
    def test_get_webhook_stripe_url(self):
        url = reverse("stripe-webhook")
        response = self.client.get(url)
        status_code = response.status_code
        self.assertEquals(resolve(url).func, stripe_webhook)
        self.assertEqual(status_code, 405)
    def test_post_webhook_stripe_url(self):
        url = reverse("stripe-webhook")
        response = self.client.post(url)
        status_code = response.status_code
        self.assertEquals(resolve(url).func, stripe_webhook)
        self.assertEqual(status_code, 405)
    
class TestProducts(TestCase):

    def setUp(self):
        self.stripe_product_id = settings.STRIPE_PRODUCT_ID
        self.stripe_price_id = settings.STRIPE_PRICE_ID
        self.product = Product.objects.create(name="Ticket", stripe_product_id=self.stripe_product_id, stock=50)
        self.price = Price.objects.create(product=self.product, stripe_price_id=self.stripe_price_id, price=10)
    def test_product_str(self):
        self.assertEqual(str(self.product), "Ticket")
    def test_product_stock(self):
        stock = int(settings.STOCK)
        self.assertEqual(self.product.stock, stock)
        url = reverse("checkout")
        for i in range(stock+1):
            response = self.client.post(url, {"quantity": 1, "price": self.price.price})
        self.assertEqual(response.status_code, 201)
            
