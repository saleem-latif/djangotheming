"""
Module to hold all the nuts and bolts for theming a django site.
"""
__version__ = "0.1.0"

from .core import is_enabled, get_base_dir, get_themes

default_app_config = "theming.apps.ThemingConfig"  # pylint: disable=invalid-name
