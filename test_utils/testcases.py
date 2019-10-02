"""
Module containing functions and methods common to all theme related tests.
"""
from __future__ import absolute_import

from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):
    """
    Base test case for theme tests.
    """
