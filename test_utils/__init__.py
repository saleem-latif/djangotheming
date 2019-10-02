"""
Utility functions for theming tests.
"""
from __future__ import absolute_import

import os

from path import Path

from django.conf import settings

# Constants common to all themes
TEMPLATE_DIR = Path(settings.BASE_DIR) / 'templates'
THEME_BASE_DIR = settings.THEMING['DIRS'][0]

# Constants for `Test Theme`.
TEST_THEME = 'test-theme'
TEST_THEME_DIR = THEME_BASE_DIR / 'test-theme'
TEST_THEME_STATIC_FILES_DIR = THEME_BASE_DIR / 'test-theme' / 'static'
TEST_THEME_TEMPLATES_DIRS = [THEME_BASE_DIR / 'test-theme' / 'templates']

# Constants for `Blue Theme`.
BLUE_THEME = 'blue-theme'
BLUE_THEME_DIR = THEME_BASE_DIR / 'blue-theme'
BLUE_THEME_STATIC_FILES_DIR = THEME_BASE_DIR / 'blue-theme' / 'static'
BLUE_THEME_TEMPLATES_DIRS = [THEME_BASE_DIR / 'blue-theme' / 'templates']

# Constants for a non existent theme.
# This theme does not exist we want these constants to simulate invalid theme settings scenario.
INVALID_THEME_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
INVALID_THEME = 'invalid-theme'
