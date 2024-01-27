import schedule
import time

from django.core.management.base import BaseCommand

from data_pull.services import update_data_from_third_party_api
from common.logging_helper import cron_logging

def job():
    update_data_from_third_party_api()
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    BaseCommand().stdout.write(BaseCommand().style.SUCCESS(f"Data pulling finished at: {timestamp}"))
    cron_logging.logger.info("Data pulling finished at: %s", timestamp)

class Command(BaseCommand):
    help = 'Update data from the third-party API'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Started pulling data'))
        schedule.every().minute.at(":00").do(job)
        while True:
            schedule.run_pending()
            time.sleep(1)
