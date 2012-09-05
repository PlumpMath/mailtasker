from django.core.management.base import BaseCommand, CommandError
from apps.mt.mail import create_route 

class Command(BaseCommand):
    help = 'Creates the basic route for receiving MailGun mail.'

    def handle(self, *args, **options):
        result = create_route()
        self.stdout.write(result.text)