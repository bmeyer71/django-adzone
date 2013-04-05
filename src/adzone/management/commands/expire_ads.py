from django.core.management.base import NoArgsCommand
from django.utils import timezone

from adzone.models import AdBase

class Command(NoArgsCommand):
    help = 'Disable ads that have expired.'

    def handle_noargs(self, **options):
        ads = AdBase.objects.filter(enabled=True)
        for ad in ads:
            if ad.ad_expiry and ad.ad_expiry < timezone.now():
                ad.enabled = False
                ad.save()
