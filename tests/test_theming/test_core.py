"""
Module containing tests for theming core.
"""
import os

import ddt
from path import Path

from django.test import override_settings

from test_utils import INVALID_THEME_DIR, TEST_THEME_DIR, TEST_THEME, INVALID_THEME, TEST_THEME_TEMPLATES_DIRS, \
    BLUE_THEME, BLUE_THEME_TEMPLATES_DIRS, THEME_BASE_DIR
from test_utils.testcases import TestCase
from theming import core
from theming import models


@ddt.ddt
class CoreTests(TestCase):
    """
    Core theming tests.
    """

    @ddt.data(
        ({'DIRS': [], 'ENABLED': True}, True),
        ({'DIRS': [], 'ENABLED': False}, False),
    )
    @ddt.unpack
    def test_is_enabled(self, theme_settings, expected):
        """
        Verify that is_enabled works as expected.
        """
        with override_settings(THEMING=theme_settings):
            self.assertEqual(
                core.is_enabled(),
                expected
            )

    @ddt.data(
        (TEST_THEME_DIR, True),
        (INVALID_THEME_DIR, False),
    )
    @ddt.unpack
    def test_is_theme_dir(self, _dir, expected):
        """
        Verify that is_theme_dir works as expected.
        """
        self.assertEqual(
            core.is_theme_dir(_dir),
            expected
        )

    def test_get_theme_base_dirs(self):
        """
        Verify that get_theme_base_dirs works as expected.
        """
        self.assertListEqual(
            core.get_theme_base_dirs(),
            [THEME_BASE_DIR]
        )

    @ddt.data(
        (INVALID_THEME, ''),
        (TEST_THEME, Path(os.path.dirname(TEST_THEME_DIR))),
    )
    @ddt.unpack
    def test_get_base_dir(self, theme, expected):
        """
        Verify that get_base_dir works as expected.
        """
        self.assertEqual(
            core.get_base_dir(theme),
            expected
        )

    def test_get_all_theme_template_dirs(self):
        """
        Verify that get_all_theme_template_dirs works as expected.
        """
        self.assertListEqual(
            sorted(core.get_all_theme_template_dirs()),
            sorted(TEST_THEME_TEMPLATES_DIRS + BLUE_THEME_TEMPLATES_DIRS)
        )

    @ddt.data(
        (THEME_BASE_DIR, [models.Theme(name=BLUE_THEME), models.Theme(name=TEST_THEME)]),
        (INVALID_THEME_DIR, []),
        (None, [models.Theme(name=BLUE_THEME), models.Theme(name=TEST_THEME)]),
    )
    @ddt.unpack
    def test_get_themes(self, themes_dir, expected):
        """
        Verify that get_themes works as expected.
        """
        self.assertEqual(
            set(core.get_themes(themes_dir)),
            set(expected)
        )
