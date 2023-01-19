from concert.models import Product, Price
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Créer un produit et un prix"

    def handle(self, *args, **options):
        print("https://dashboard.stripe.com/test/products/")
        name = input("Entrer le nom du produit: ")
        stripe_product_id = input("Entre le stripe_product_id: ")
        product = Product.objects.create(name=name, stripe_product_id=stripe_product_id)
        print("Produit créé avec succès")
        price = input("Entrer le prix du produit: ")
        stripe_price_id = input("Entrer le stripe_price_id: ")
        Price.objects.create(product=product, price=price, stripe_price_id=stripe_price_id)
        print("Prix créé avec succès")
        self.stdout.write(self.style.SUCCESS("Produit et prix créés avec succès"))
