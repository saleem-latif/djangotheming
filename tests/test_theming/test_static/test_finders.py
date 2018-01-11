"""
Tests for theme static files finders.
"""
import ddt

from django.core.checks import Error
from django.test import override_settings

from test_utils import BLUE_THEME, BLUE_THEME_STATIC_FILES_DIR, TEST_THEME, TEST_THEME_DIR, TEST_THEME_STATIC_FILES_DIR
from test_utils.testcases import TestCase
from theming.static.finders import ThemeFilesFinder


@ddt.ddt
class TestThemeFilesFinder(TestCase):
    """
    Test theming static files finders.
    """

    def setUp(self):
        """
        Setup TestThemeFilesFinder instance.
        """
        super(TestThemeFilesFinder, self).setUp()
        self.finder = ThemeFilesFinder()

    def test_find_first_themed_asset(self):
        """
        Verify Theme Finder returns themed assets
        """
        asset = "test-theme/styles.css"
        match = self.finder.find(asset)

        self.assertEqual(match, TEST_THEME_DIR / "static" / "styles.css")

    def test_find_all_themed_asset(self):
        """
        Verify Theme Finder returns themed assets
        """
        asset = "test-theme/styles.css"
        matches = self.finder.find(asset, all=True)

        # Make sure only first match was returned
        self.assertEqual(1, len(matches))

        self.assertEqual(matches[0], TEST_THEME_DIR / "static" / "styles.css")

    @ddt.data(
        ('test-theme', 'styles.css', TEST_THEME_DIR / "static" / "styles.css"),
        ('test-theme', 'images/spinning.gif', None),
    )
    @ddt.unpack
    def test_find_in_theme(self, theme, asset, expected):
        """
        Verify find in theme method of finders returns asset from specified theme
        """
        self.assertEqual(
            self.finder.find_in_theme(theme, asset),
            expected
        )

    @ddt.data(
        (
            {},
            [
                Error(
                    'The THEMING["DIRS"] setting must be populated.',
                    id='theming.static.E001',
                )
            ]

        ),
        (
            {'DIRS': None},
            [
                Error(
                    'The THEMING["DIRS"] setting is not a tuple or list.',
                    hint='Perhaps you forgot a trailing comma?',
                    id='theming.static.E002',
                )
            ]

        ),
        (
            {'DIRS': [None]},
            [
                Error(
                    'THEMING["DIRS"] must contain only strings.',
                    id='theming.static.E003',
                )
            ]

        ),
        (
            {'DIRS': ['../invalid/relative/path']},
            [
                Error(
                    'THEMING["DIRS"] must contain only absolute paths to themes dirs.',
                    id='theming.static.E004',
                )
            ]

        ),
        (
            {'DIRS': ['/invalid/absolute/relative/path']},
            [
                Error(
                    'THEMING["DIRS"] must contain valid paths.',
                    id='theming.static.E005',
                )
            ]

        )
    )
    @ddt.unpack
    def test_check(self, theming_overrides, expected):
        """
        Verify check returns appropriate errors in case of invalid settings.
        """
        with override_settings(THEMING=theming_overrides):
            self.assertEqual(
                self.finder.check(),
                expected,
            )

    def test_list(self):
        """
        Verify list returns all themed assets and corresponding storage class.
        """
        expected = {
            ('styles.css', TEST_THEME, TEST_THEME_STATIC_FILES_DIR),
            ('styles.css', BLUE_THEME, BLUE_THEME_STATIC_FILES_DIR),
        }
        results = self.finder.list(ignore_patterns=None)
        theme_assets = set(map(lambda item: (item[0], item[1].prefix, item[1].location), results))

        self.assertEqual(
            theme_assets,
            expected
        )
