from django.db import models
from adzone.models import *

class AdManager(models.Manager):
    """ A Custom Manager for ads """

    def get_random_ad(self, ad_category, ad_zone):
        """
        Returns a random advert that belongs to the specified category and zone
        
        """
        try:
            ads = self.get_query_set().filter(category__slug=ad_category, zone__slug=ad_zone).order_by('?')
        except IndexError:
            return None;
        else:
            for ad in ads:
                ic = len(AdImpression.objects.filter(ad=ad))
                if ad.impression_limit < ic:
                    return ad
