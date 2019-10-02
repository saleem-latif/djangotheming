"""
Module to hold all the nuts and bolts for theming a django site.
"""
from __future__ import absolute_import

from .core import get_base_dir, get_themes, is_enabled

__version__ = "2.0.1"


default_app_config = "theming.apps.ThemingConfig"  # pylint: disable=invalid-name
