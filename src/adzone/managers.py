from django.db import models


class AdManager(models.Manager):
    """ A Custom Manager for ads """

    def get_random_ad(self, ad_zone, ad_category=None):
        """
        Returns a random advert that belongs for the specified ``ad_category``
        and ``ad_zone``.
        If ``ad_category`` is None, the ad will be category independent.
        """
        from adzone.models import AdImpression
        ad = None
        try:
            if ad_category:
                ads = self.get_query_set().filter(
                    category__slug=ad_category,
                    enabled=True,
                    zone__slug=ad_zone).order_by('?')
                if ads != []:
                    for item in ads:
                        if item.impression_limit == 0:
                            ad = item
                        else:
                            if AdImpression.objects.filter(ad_id=item.id).count() > item.impression_limit:
                                ad = None
                                continue
                            else:
                                ad = item
                                break
            else:
                ads = self.get_query_set().filter(
                    enabled=True,
                    zone__slug=ad_zone).order_by('?')
                if ads != []:
                    for item in ads:
                        if item.impression_limit == 0:
                            ad = item
                        else:
                            if AdImpression.objects.filter(ad_id=item.id).count() > item.impression_limit:
                                ad = None
                                continue
                            else:
                                ad = item
                                break

        except IndexError:
            return None
        return ad
