from django.core.management import BaseCommand, call_command

from chat.models import User

class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of data for testing purposes"

    def handle(self, *args, **kwargs):
        call_command('loaddata','initial_data')
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()