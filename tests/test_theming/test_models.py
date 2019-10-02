# pylint: disable=no-member
"""
Validate theming models.
"""
from __future__ import absolute_import

from functools import partial

import ddt

from django.conf import settings
from django.test import override_settings

from test_utils import TEST_THEME_TEMPLATES_DIRS, THEME_BASE_DIR
from test_utils.factories import SiteFactory, ThemeFactory
from test_utils.testcases import TestCase
from theming.models import Theme


@ddt.ddt
class TestModels(TestCase):
    """
    Test Theming model definitions.
    """

    def setUp(self):
        """
        Setup model instance.
        """
        self.theme = ThemeFactory(name='test-theme', site__domain='test-theme')

    @ddt.data(
        (
            partial(ThemeFactory, name='test-theme', site__domain='test-theme'),
            partial(ThemeFactory, name='blue-theme', site__domain='blue-theme'),
            False
        ),
        (
            partial(ThemeFactory, name='test-theme', site__domain='test-theme'),
            partial(ThemeFactory, name='test-theme', site__domain='test-theme'),
            True
        )
    )
    @ddt.unpack
    def test_equality(self, first_theme_factory, second_theme_factory, expected):
        """
        Validate that themes can be compared for equality
        """
        self.assertEqual(
            first_theme_factory() == second_theme_factory(),
            expected
        )

    @ddt.data(
        (
            partial(ThemeFactory, name='test-theme', site__domain='test-theme'),
            partial(ThemeFactory, name='blue-theme', site__domain='blue-theme'),
            True
        ),
        (
            partial(ThemeFactory, name='test-theme', site__domain='test-theme'),
            partial(ThemeFactory, name='test-theme', site__domain='test-theme'),
            False
        )
    )
    @ddt.unpack
    def test_inequality(self, first_theme_factory, second_theme_factory, expected):
        """
        Validate that themes can be compared for inequality
        """
        self.assertEqual(
            first_theme_factory() != second_theme_factory(),
            expected
        )

    def test_hash(self):
        """
        Validate that themes can be compared for inequality
        """
        self.assertEqual(
            hash(self.theme),
            hash((self.theme.name, self.theme.path))
        )

    def test_str(self):
        """
        Validate string representation for theme.
        """
        self.assertEqual(
            str(self.theme),
            u"<Theme: {name} at '{path}'>".format(name=self.theme.name, path=self.theme.path)
        )

    def test_repr(self):
        """
        Validate representation for theme.
        """
        self.assertEqual(
            repr(self.theme),
            u"<Theme: {name} at '{path}'>".format(name=self.theme.name, path=self.theme.path)
        )

    def test_base_dir(self):
        """
        Validate base_dir property of theme returns correct path.
        """
        self.assertEqual(
            self.theme.base_dir,
            THEME_BASE_DIR,
        )

    def test_template_dirs(self):
        """
        Validate template_dirs property of theme returns correct path.
        """
        self.assertEqual(
            self.theme.template_dirs,
            TEST_THEME_TEMPLATES_DIRS,
        )

    def test_get_theme(self):
        """
        Validate get_theme returns correct theme.
        """
        self.assertEqual(
            Theme.get_theme(self.theme.site),
            self.theme
        )

    def test_get_theme_when_theme_does_not_exist(self):  # pylint: disable=invalid-name
        """
        Validate get_theme returns default theme if site has no associated theme.
        """
        site = SiteFactory(domain='blue-theme')

        # Make sure there is not theme with the above site
        Theme.objects.filter(site=site).delete()  # pylint: disable=no-member

        self.assertEqual(
            Theme.get_theme(site),
            Theme(name=settings.THEMING['DEFAULT'], site=site)
        )

    def test_get_theme_when_theme_does_not_exist_and_no_default_theme(self):  # pylint: disable=invalid-name
        """
        Validate get_theme returns Noneif site has no associated theme and there is not default theme.
        """
        site = SiteFactory(domain='blue-theme')

        # Make sure there is not theme with the above site
        Theme.objects.filter(site=site).delete()  # pylint: disable=no-member

        with override_settings(THEMING=dict(settings.THEMING, DEFAULT=None)):
            self.assertEqual(
                Theme.get_theme(site),
                None,
            )
