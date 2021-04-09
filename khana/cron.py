from .models import TempUser, Date
import datetime
from django.utils import timezone


# def my_scheduled_job():
#     Test.objects.create(name='test')


def expire_temp_user():
    # TempUser.objects.filter(created__lt=timezone.now() - datetime.timedelta(days=2)).delete()
    TempUser.objects.filter(created__lt=timezone.now() - datetime.timedelta(days=3)).delete()

def expire_old_orders():
    date_30_days_ago = timezone.now().date()-datetime.timedelta(days=30)
    Date.objects.filter(date__lte=date_30_days_ago).delete()