from django.core.management.base import BaseCommand
from data_pull.services import update_data_from_third_party_api

class Command(BaseCommand):
    help = 'Update data from the third-party API'

    def handle(self, *args, **kwargs):
        update_data_from_third_party_api()
        self.stdout.write(self.style.SUCCESS('Data update completed successfully'))
