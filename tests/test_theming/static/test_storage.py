"""
Tests for theme static files storage classes.
"""
import ddt

from django.test import TestCase, override_settings
from django.conf import settings

from theming.static.storage import ThemeStorage

from test_utils import TEST_THEME_STATIC_FILES_DIR, TEST_THEME, BLUE_THEME
from test_utils.utils import setup_current_theme
from test_utils.factories import ThemeFactory


@ddt.ddt
@override_settings(DEBUG=True)
class TestThemeStorageDebugMode(TestCase):
    """
    Test theming static files storage.
    """

    def setUp(self):
        """
        Setup theme storage and current theme.
        """
        super(TestThemeStorageDebugMode, self).setUp()
        self.storage = ThemeStorage(location=TEST_THEME_STATIC_FILES_DIR)
        self.theme = ThemeFactory(name=TEST_THEME)
        setup_current_theme(self.theme)

    @ddt.data(
        (TEST_THEME, 'styles.css', True),
        (BLUE_THEME, 'styles.css', True),
        (TEST_THEME, 'images/spinning.gif', False),
        ('non-existing-theme', 'styles.css', False),
    )
    @ddt.unpack
    def test_themed(self, theme, asset, expected):
        """
        Verify storage returns True on themed assets
        """
        self.assertEqual(
            self.storage.themed(asset, theme),
            expected
        )

    @override_settings(THEMING=dict(settings.THEMING, ENABLED=False))
    def test_themed_with_theming_disabled(self):
        """
        Verify storage returns True on themed assets
        """
        self.assertEqual(
            self.storage.themed(TEST_THEME, 'styles.css'),
            False
        )

    @ddt.data(
        ('styles.css', settings.STATIC_URL + TEST_THEME + '/styles.css'),
        ('images/spinning.gif', settings.STATIC_URL + 'images/spinning.gif'),
    )
    @ddt.unpack
    def test_url(self, asset, expected):
        """
        Verify storage returns correct url depending upon the enabled theme
        """
        self.assertEqual(
            self.storage.url(asset),
            expected,
        )


@ddt.ddt
@override_settings(DEBUG=False)
class TestThemeStorageProductionMode(TestCase):
    """
    Test theming static files storage.
    """

    def setUp(self):
        """
        Setup theme storage.
        """
        super(TestThemeStorageProductionMode, self).setUp()
        self.storage = ThemeStorage(location=settings.STATIC_ROOT)

    @ddt.data(
        (TEST_THEME, 'styles.css', True),
        (BLUE_THEME, 'styles.css', True),
        (TEST_THEME, 'images/spinning.gif', False),
        ('non-existing-theme', 'styles.css', False),
    )
    @ddt.unpack
    def test_themed(self, theme, asset, expected):
        """
        Verify storage returns True on themed assets
        """
        self.assertEqual(
            self.storage.themed(asset, theme),
            expected
        )

    @override_settings(THEMING=dict(settings.THEMING, ENABLED=False))
    def test_themed_with_theming_disabled(self):
        """
        Verify storage returns True on themed assets
        """
        self.assertEqual(
            self.storage.themed(TEST_THEME, 'styles.css'),
            False
        )


@ddt.ddt
@override_settings(DEBUG=False)
class TestThemeStorageCollectStaticMode(TestCase):
    """
    Test theming static files storage.
    """

    def setUp(self):
        """
        Setup theme storage and current theme.
        """
        super(TestThemeStorageCollectStaticMode, self).setUp()
        self.storage = ThemeStorage(location=settings.STATIC_ROOT, prefix=TEST_THEME)

        # In collectstatic run there won't be a current theme.
        setup_current_theme(None)

    @ddt.data(
        ('styles.css', settings.STATIC_URL + TEST_THEME + '/styles.css'),
        ('images/spinning.gif', settings.STATIC_URL + 'images/spinning.gif'),
    )
    @ddt.unpack
    def test_url(self, asset, expected):
        """
        Verify storage returns correct url depending upon the enabled theme
        """
        self.assertEqual(
            self.storage.url(asset),
            expected,
        )
