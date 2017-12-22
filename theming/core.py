"""
Core logic for Theming.
"""
import os

from path import Path

from django.conf import settings


def is_enabled():
    """
    Return `True` if theming is enabled, return `False` otherwise.
    """
    return settings.THEMING.get('ENABLED', False)


def is_theme_dir(_dir):
    """
    Return true if given dir is a theme directory, returns False otherwise.

    A theme dir must have subdirectory 'static' or 'templates' or both.

    Arguments:
        _dir: directory path to check for a theme

    Returns:
        Returns true if given dir is a theme directory.
    """
    theme_sub_directories = {'static', 'templates'}
    return bool(os.path.isdir(_dir) and theme_sub_directories.intersection(os.listdir(_dir)))


def get_theme_base_dirs():
    """
    Return a list of all directories that contain themes.

    Example:
        >> get_theme_base_dirs()
        ['/var/themes/']

    Returns:
         (list): list of theme base directories
    """
    return [Path(theme_dir) for theme_dir in settings.THEMING['DIRS']]


def get_base_dir(name):
    """
    Return absolute path to the directory that contains the given theme.

    Arguments:
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

    Arguments:
        themes_dir (str): (Optional) Path to themes base directory

    Returns:
        list of themes known to the system.
    """
    # TODO: Fix this
    # Importing here to avoid circular import
    from theming.models import Theme

    themes_dirs = [Path(themes_dir)] if themes_dir else get_theme_base_dirs()
    # pick only directories and discard files in themes directory
    themes = []

    for _dir in themes_dirs:
        themes.extend(
            [Theme(name=name) for name in os.listdir(_dir) if is_theme_dir(Path(_dir) / name)]
        )

    return themes
