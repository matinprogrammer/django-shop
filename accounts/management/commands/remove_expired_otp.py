from django.core.management import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
import pytz


class Command(BaseCommand):
    help = 'Remove expired OTP codes'

    def handle(self, *args, **options):
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
        OtpCode.objects.filter(created__lte=expired_time).delete()
        self.stdout.write('all expired OTP codes have been removed')