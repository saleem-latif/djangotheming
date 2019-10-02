"""
Theming Factories.
"""
from __future__ import absolute_import

import factory
from factory.django import DjangoModelFactory

from django.contrib.sites.models import Site

from theming.models import Theme


class SiteFactory(DjangoModelFactory):
    """
    Factory for django.contrib.sites.models.Site.
    """

    class Meta:
        model = Site
        django_get_or_create = ('domain',)

    name = "test site"
    domain = "testserver"


class ThemeFactory(DjangoModelFactory):
    """
    Factory for theming.models.Theme.
    """

    class Meta:
        model = Theme
        django_get_or_create = ('site',)

    site = factory.SubFactory(SiteFactory)
    name = "test-theme"
