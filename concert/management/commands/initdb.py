from concert.models import Product, Price
from django.core.management.base import BaseCommand
import os
from django.conf import settings


class Command(BaseCommand):
    help = "Créer un produit et un prix pour les tests"

    def handle(self, *args, **options):
        if settings.PROD:
            stripe_product_id = os.environ.get("STRIPE_PRODUCT_ID")
            stripe_price_id = os.environ.get("STRIPE_PRICE_ID")
        else:
            stripe_product_id = "prod_Me1k1TJJqAUbNH"
            stripe_price_id = "price_1LujhEFo3msg8YF5NiXH1IYk"
        product = Product.objects.create(name="Ticket", stripe_product_id=stripe_product_id, stock=50)
        Price.objects.create(product=product, price=5, stripe_price_id=stripe_price_id)
        self.stdout.write(self.style.SUCCESS("Produit et prix créés avec succès"))