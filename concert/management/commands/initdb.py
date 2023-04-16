from concert.models import Product, Price
from django.core.management.base import BaseCommand
import os
from django.conf import settings


class Command(BaseCommand):
    help = "Créer un produit et un prix pour les tests"

    def handle(self, *args, **options):
        print("Création du produit et du prix")
        for i in range(3):
            name = input("Nom du produit: ")
            price = input("Prix du produit: ")
            stock = input("Stock du produit: ")
            product_id = input("ID du produit: ")
            product = Product.objects.create(name=name, stock=stock, stripe_product_id=product_id)
            price_id = input("ID du prix: ")
            Price.objects.create(product=product, stripe_price_id=price_id, price=price)
            print("Enregistré...")
