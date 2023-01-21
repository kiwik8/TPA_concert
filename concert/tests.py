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
        if settings.PROD is True:
            self.stripe_product_id = os.environ.get("STRIPE_PRODUCT_ID")
            self.stripe_price_id = os.environ.get("STRIPE_PRICE_ID")
            self.product = Product.objects.create(name="Ticket", stripe_product_id=self.stripe_product_id, stock=50)
            self.price = Price.objects.create(product=self.product, stripe_price_id=self.stripe_price_id, price=10)
        else:
            self.product = Product.objects.create(name="Ticket", stripe_product_id="prod_Me1k1TJJqAUbNH", stock=50)
            self.price = Price.objects.create(product=self.product, stripe_price_id="price_1LujhEFo3msg8YF5NiXH1IYk", price=10)

    def test_index_url(self):
        url = reverse('index')
        response = self.client.get(url)
        status_code = response.status_code
        self.assertEquals(resolve(url).func, redirect_to)
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, "concert/homepage.html")
    def test_home_url(self):
        url = reverse('home')
        response = self.client.get(url)
        status_code = response.status_code
        self.assertTrue("redirected" in response.cookies)
        self.assertEquals(resolve(url).func, redirect_to)
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, "concert/homepage.html")
    def test_homepage_url(self):
        url = reverse('homepage')
        response = self.client.get(url)
        status_code = response.status_code
        self.assertEquals(resolve(url).func, homepage)
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, "concert/homepage.html")
        url = reverse('index')
        response = self.client.get(url)
        self.assertFalse("redirected" in response.cookies)
        self.assertTemplateUsed(response, "concert/index.html")
    def test_get_subscribe_url(self):
        url = reverse('subscribe')
        response = self.client.get(url)
        status_code = response.status_code
        self.assertEquals(resolve(url).func, subscribe)
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, "concert/cancel.html")
    def test_post_subscribe_url(self):
        url = reverse("subscribe")
        email = "test@gmail.com"
        response = self.client.post(url, {"email": email})
        client = Client.objects.get(email=email)
        status_code = response.status_code
        self.assertEquals(resolve(url).func, subscribe)
        self.assertEqual(status_code, 200)
        self.assertEqual(client.email, email)
        self.assertTemplateUsed(response, "concert/success.html")
    def test_get_create_checkout_session_url(self):
        url = reverse("create-checkout-session")
        response = self.client.get(url)
        status_code = response.status_code
        self.assertEquals(resolve(url).func.view_class, CreateCheckoutSessionView)
        self.assertEqual(status_code, 405)
    def test_post_create_checkout_session_url(self):
        url = reverse("create-checkout-session")
        context = {"quantity": 1}
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
        if settings.PROD is True:
            self.stripe_product_id = os.environ.get("STRIPE_PRODUCT_ID")
            self.stripe_price_id = os.environ.get("STRIPE_PRICE_ID")
            self.product = Product.objects.create(name="Ticket", stripe_product_id=self.stripe_product_id, stock=50)
            self.price = Price.objects.create(product=self.product, stripe_price_id=self.stripe_price_id, price=10)
        else:
            self.product = Product.objects.create(name="Ticket", stripe_product_id="prod_Me1k1TJJqAUbNH", stock=50)
            self.price = Price.objects.create(product=self.product, stripe_price_id="price_1LujhEFo3msg8YF5NiXH1IYk", price=10)

    def test_product(self):
        self.assertEqual(self.product.name, "Ticket")
        self.assertEqual(self.product.stripe_product_id, "prod_Me1k1TJJqAUbNH")
    def test_price(self):
        self.assertEqual(self.price.product.name, "Ticket")
        self.assertEqual(self.price.stripe_price_id, "price_1LujhEFo3msg8YF5NiXH1IYk")
        self.assertEqual(self.price.price, 10)
    def test_product_str(self):
        self.assertEqual(str(self.product), "Ticket")
    def test_product_stock(self):
        stock = int(settings.STOCK)
        self.assertEqual(self.product.stock, stock)
        url = reverse("create-checkout-session")
        for i in range(stock+1):
            response = self.client.post(url, {"quantity": 1})
        self.assertEqual(response.status_code, 201)
            
