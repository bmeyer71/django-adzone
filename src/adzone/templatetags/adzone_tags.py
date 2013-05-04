# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from datetime import datetime
from django import template
from adzone.models import AdBase, AdImpression

from django.utils import timezone
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

import re

register = template.Library()


@register.inclusion_tag('adzone/ad_tag.html', takes_context=True)
def random_zone_ad(context, ad_zone):
    """
    Returns a random advert for ``ad_zone``.
    The advert returned is independent of the category

    In order for the impression to be saved add the following
    to the TEMPLATE_CONTEXT_PROCESSORS:

    'adzone.context_processors.get_source_ip'

    Tag usage:
    {% load adzone_tags %}
    {% random_zone_ad 'zone_slug' %}

    """
    to_return = {}

    # Retrieve a random ad for the zone
    ad = AdBase.objects.get_random_ad(ad_zone)
    to_return['ad'] = ad

    # Record a impression for the ad
    if context.has_key('from_ip') and ad:
        from_ip = context.get('from_ip')
        try:
            impression = AdImpression(
                    ad=ad,
                    impression_date=timezone.now(),
                    source_ip=from_ip
            )
            impression.save()
        except:
            pass
    to_return['request'] = context['request']
    return to_return


@register.inclusion_tag('adzone/ad_tag.html', takes_context=True)
def random_category_ad(context, ad_zone, ad_category):
    """
    Returns a random advert from the specified category.

    Usage:
    {% load adzone_tags %}
    {% random_category_ad 'zone_slug' 'my_category_slug' %}

    """
    to_return = {}

    # Retrieve a random ad for the category and zone
    #~ ads = AdBase.objects.get_random_ad(ad_category, ad_zone)
    #~ ad = None

    #~ for a in ads:
        #~ ic = len(AdImpression.objects.filter(ad=a))
        #~ if ic < a.impression_limit:
            #~ ad = a
            #~ break

    ad = AdBase.objects.get_random_ad(ad_zone, ad_category)

    to_return['ad'] = ad
    to_return['request'] = context["request"]
    
    # Record a impression for the ad
    if context.has_key('from_ip') and ad:
        from_ip = context.get('from_ip')
        try:
            impression = AdImpression(
                    ad=ad,
                    impression_date=timezone.now(),
                    source_ip=from_ip
            )
            impression.save()
        except:
            pass
    return to_return

@register.simple_tag(takes_context=True)
def url_keyword(context, link_ad):
    ad_text = link_ad.textad.content
    request = context['request']
    try:
        ad_keyword = re.search(r"\[\[(.*?)\]\]", ad_text)
    except:
        return ad_text

    if ad_keyword == None:
        return ad_text
    else:
        keyword = ad_keyword.group(1)

    text = ad_text.split(ad_keyword.group(0))
    if request.user.is_superuser:
        ad_url = reverse('admin:adzone_textad_change', args=(link_ad.id,))
    else:
        ad_url = reverse('adzone_ad_view', args=(link_ad.id,))

    result = '<p>%s<a target="_blank" href="%s" class="adText">%s</a>%s</p>' % (text[0], ad_url, keyword, text[1])
    return mark_safe(result)
