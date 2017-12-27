"""
Factories module to hold theming factories
"""
import factory

from django.contrib.sites.models import Site
from factory.django import DjangoModelFactory

from theming.models import Theme


class SiteFactory(DjangoModelFactory):
    """
    Factory for django.contrib.sites.models.Site
    """
    class Meta(object):
        model = Site
        django_get_or_create = ('domain',)

    name = "test site"
    domain = "testserver"


class ThemeFactory(DjangoModelFactory):
    """
    Factory for django.contrib.sites.models.Site
    """
    class Meta(object):
        model = Theme
        django_get_or_create = ('site',)

    site = factory.SubFactory(SiteFactory)
    name = "test-theme"
