"""
Tests for theme template loaders.
"""
from functools import partial

import ddt

from django.template.engine import Engine

from test_utils import BLUE_THEME_TEMPLATES_DIRS, TEMPLATE_DIR, TEST_THEME_TEMPLATES_DIRS
from test_utils.factories import ThemeFactory
from test_utils.testcases import TestCase
from test_utils.utils import cleanup_current_request_and_theme, setup_current_theme
from theming.template.loaders.theme import Loader


@ddt.ddt
class TestLoader(TestCase):
    """
    Test theming static files finders.
    """

    def setUp(self):
        """
        Setup Loader instance.
        """
        super(TestLoader, self).setUp()
        self.engine = Engine(
            dirs=[TEMPLATE_DIR],
            loaders=[
                'theming.template.loaders.theme.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        )

        self.loader = Loader(engine=self.engine)
        self.addCleanup(cleanup_current_request_and_theme)

    def test_get_dirs(self):
        """
        Verify Theme template loader return all theme template dirs.
        """
        expected = {TEMPLATE_DIR}.union(TEST_THEME_TEMPLATES_DIRS).union(BLUE_THEME_TEMPLATES_DIRS)
        template_dirs = self.loader.get_dirs()

        self.assertEqual(
            set(template_dirs),
            expected,
        )

    @ddt.data(
        (
            partial(ThemeFactory, name='test-theme', site__domain='test-theme'),
            {TEMPLATE_DIR}.union(TEST_THEME_TEMPLATES_DIRS)
        ),
        (
            partial(ThemeFactory, name='blue-theme', site__domain='blue-theme'),
            {TEMPLATE_DIR}.union(BLUE_THEME_TEMPLATES_DIRS)
        ),
    )
    @ddt.unpack
    def test_get_dirs_inside_request(self, theme_factory, expected):
        """
        Verify Theme template loader return current theme template dirs when accessed within an ongoing request.
        """
        # Create theme instance
        theme = theme_factory()
        setup_current_theme(theme)

        template_dirs = self.loader.get_dirs()

        self.assertEqual(
            set(template_dirs),
            expected,
        )

    def test_get_dirs_inside_request_with_no_theme(self):  # pylint: disable=invalid-name
        """
        Verify Theme template loader return default template dirs when accessed within a request with no theme.
        """
        setup_current_theme(theme=None)

        template_dirs = self.loader.get_dirs()

        self.assertEqual(
            set(template_dirs),
            {TEMPLATE_DIR},
        )
