from concert.models import Client, Question
from django.core.management.base import BaseCommand
import random
import string

class Command(BaseCommand):
    help = "Permet de peupler la base de données avec des données de test"

    def handle(self, *args, **options):
        first_names=('John','Andy','Joe', "Tom", "Antoine", "Lucie", "Ben")
        last_names=('Johnson','Smith','Williams', "Demoulin", "Sa", "Doe")
        mail_providers = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "mail.com", "icloud.com"]
        username = ''.join(random.choices(string.ascii_lowercase, k=7))
        nb = input("Combien de clients voulez-vous créer ? ")
        for i in range(1, int(nb)):
            username = ''.join(random.choices(string.ascii_lowercase, k=7))
            first_name, last_name = random.choice(first_names), random.choice(last_names)
            email = username + "@" + random.choice(mail_providers)
            Client.objects.create(email=email)
            Question.objects.create(email=email, fisrt_name=first_name, last_name=last_name, message="Question de test")
            print("Client : {} {} créé avec succès".format(first_name, last_name))
        self.stdout.write(self.style.SUCCESS("Clients créés avec succès"))

    

