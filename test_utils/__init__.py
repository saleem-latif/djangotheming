"""
Utility functions for theming tests.
"""

import os
from path import Path

from django.conf import settings

TEMPLATE_DIR = Path(settings.BASE_DIR) / 'templates'
THEME_BASE_DIR = settings.THEMING['DIRS'][0]

# Test theme constants
TEST_THEME = 'test-theme'
TEST_THEME_DIR = THEME_BASE_DIR / 'test-theme'
TEST_THEME_STATIC_FILES_DIR = THEME_BASE_DIR / 'test-theme' / 'static'
TEST_THEME_TEMPLATES_DIRS = [THEME_BASE_DIR / 'test-theme' / 'templates']

# Blue theme constants
BLUE_THEME = 'blue-theme'
BLUE_THEME_DIR = THEME_BASE_DIR / 'blue-theme'
BLUE_THEME_STATIC_FILES_DIR = THEME_BASE_DIR / 'blue-theme' / 'static'
BLUE_THEME_TEMPLATES_DIRS = [THEME_BASE_DIR / 'blue-theme' / 'templates']

# Invalid theme constants
INVALID_THEME_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
INVALID_THEME = 'invalid-theme'
