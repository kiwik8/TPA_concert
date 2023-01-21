from concert.models import Product, Price
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Créer un produit et un prix pour les tests"

    def handle(self, *args, **options):
        product = Product.objects.create(name="test", stripe_product_id="test", stock=50)
        Price.objects.create(product=product, price=5, stripe_price_id="test")
        self.stdout.write(self.style.SUCCESS("Produit et prix créés avec succès"))