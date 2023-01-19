from concert.models import Client, Question
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Permet de vider la base de données"

    def handle(self, *args, **options):
        Client.objects.all().delete()
        Question.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Clients supprimés avec succès"))