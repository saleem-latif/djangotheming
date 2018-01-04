"""
Test utils
"""

import os
from path import Path

from django.conf import settings

THEME_BASE_DIR = settings.THEMING['DIRS'][0]

# Test theme constants
TEST_THEME = 'test-theme'
TEST_THEME_DIR = THEME_BASE_DIR / 'test-theme'
TEST_THEME_TEMPLATES_DIRS = [THEME_BASE_DIR / 'test-theme' / 'templates']

# Blue theme constants
BLUE_THEME = 'blue-theme'
BLUE_THEME_DIR = THEME_BASE_DIR / 'blue-theme'
BLUE_THEME_TEMPLATES_DIRS = [THEME_BASE_DIR / 'blue-theme' / 'templates']

# Invalid theme constants
INVALID_THEME_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
INVALID_THEME = 'invalid-theme'
