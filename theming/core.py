"""
Core logic for Theming.
"""
import os
from path import Path
from django.conf import ImproperlyConfigured, settings


def is_enabled():
    """
    Return `True` if theming is enabled, return `False` otherwise.
    """
    return settings.THEMING.get('ENABLED', False)


def get_theme_dirs(themes_dir=None):
    """
    Return all theme dirs in given dir.
    """
    return [_dir for _dir in os.listdir(themes_dir) if is_theme_dir(themes_dir / _dir)]


def is_theme_dir(_dir):
    """
    Returns true if given dir is a theme directory, returns False otherwise.
    A theme dir must have subdirectory 'static' or 'templates' or both.

    Args:
        _dir: directory path to check for a theme

    Returns:
        Returns true if given dir is a theme directory.
    """
    theme_sub_directories = {'static', 'templates'}
    return bool(os.path.isdir(_dir) and theme_sub_directories.intersection(os.listdir(_dir)))


def get_theme_base_dirs():
    """
    Return a list of all directories that contain themes.

    Raises:
        ImproperlyConfigured - exception is raised if
            1 - THEMING['DIRS'] is not a string
            2 - THEMING['DIRS'] is not an absolute path
            3 - path specified by THEMING['DIRS'] does not exist

    Example:
        >> get_theme_base_dirs()
        ['/var/themes/']

    Returns:
         (list): list of theme base directories
    """
    theme_dirs = settings.THEMING['DIRS']
    # TODO: handle invalid settings, i.e. missing 'DIRS'

    if not isinstance(theme_dirs, list):
        raise ImproperlyConfigured("THEMING['DIRS'] must be a list.")
    if not all([isinstance(theme_dir, str) for theme_dir in theme_dirs]):
        raise ImproperlyConfigured("THEMING['DIRS'] must contain only strings.")
    if not all([theme_dir.startswith("/") for theme_dir in theme_dirs]):
        raise ImproperlyConfigured("THEMING['DIRS'] must contain only absolute paths to themes dirs.")
    if not all([os.path.isdir(theme_dir) for theme_dir in theme_dirs]):
        raise ImproperlyConfigured("THEMING['DIRS'] must contain valid paths.")

    return [Path(theme_dir) for theme_dir in theme_dirs]


def get_base_dir(name):
    """
    Returns absolute path to the directory that contains the given theme.

    Args:
        name (str): theme directory name to get base path for
    Returns:
        (str): Base directory that contains the given theme
    """
    # TODO: handle theme not found
    for themes_dir in get_theme_base_dirs():
        if name in (_dir for _dir in os.listdir(themes_dir) if is_theme_dir(themes_dir / _dir)):
            return themes_dir

    # TODO: raise ThemeNotFound instead of returning ''
    return ''


def get_all_theme_template_dirs():
    """
    Return a list of all template directories, for all the themes.

    Example:
        >> get_all_theme_template_dirs()
        [
            '/var/themes//test-theme/templates/',
        ]

    Returns:
        (list): list of directories containing theme templates.
    """
    template_paths = list()

    for theme in get_themes():
        template_paths.extend(
            theme.template_dirs
        )
    return template_paths


def get_themes(themes_dir=None):
    """
    Return a list of all themes known to the system.
    If themes_dir is given then return only the themes residing inside that directory.

    Args:
        themes_dir (str): (Optional) Path to themes base directory
    Returns:
        list of themes known to the system.
    """
    # TODO: Fix this
    # Importing here to avoid circular import
    from theming.models import Theme

    if not is_enabled():
        return []

    themes_dirs = [Path(themes_dir)] if themes_dir else get_theme_base_dirs()
    # pick only directories and discard files in themes directory
    themes = []
    for themes_dir in themes_dirs:
        themes.extend([Theme(name=name) for name in get_theme_dirs(themes_dir)])

    return themes
