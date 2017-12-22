"""
Test utils
"""

import os
from path import Path

from django.conf import settings

# Test theme constants
TEST_THEME = 'test-theme'
TEST_THEME_DIR = settings.THEMING['DIRS'][0] / 'test-theme'
TEST_THEME_TEMPLATES_DIR = settings.THEMING['DIRS'][0] / 'test-theme' / 'templates'

# Invalid theme constants
INVALID_THEME_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
INVALID_THEME = 'invalid-theme'
