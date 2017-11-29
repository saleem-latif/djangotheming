"""
Core logic for Comprehensive Theming.
"""
from django.conf import settings

from path import Path


def enable_theming():
    """
        Add directories and relevant paths to settings for comprehensive theming.
    """
    for theme in get_themes():
        locale_dir = theme.path / "conf" / "locale"
        if locale_dir.isdir():
            settings.LOCALE_PATHS = (locale_dir, ) + settings.LOCALE_PATHS


class Theme(object):
    """
    class to encapsulate theme related information.
    """
    name = ''
    theme_dir_name = ''

    def __init__(self, name='', theme_dir_name='', theme_base_dir=None):
        """
        init method for Theme
        Args:
            name: name if the theme
            theme_dir_name: directory name of the theme
            theme_base_dir: directory path of the folder that contains the theme
        """
        self.name = name
        self.theme_dir_name = theme_dir_name
        self.theme_base_dir = theme_base_dir

    def __eq__(self, other):
        """
        Returns True if given theme is same as the self
        Args:
            other: Theme object to compare with self

        Returns:
            (bool) True if two themes are the same else False
        """
        return (self.theme_dir_name, self.path) == (other.theme_dir_name, other.path)

    def __hash__(self):
        return hash((self.theme_dir_name, self.path))

    def __unicode__(self):
        return u"<Theme: {name} at '{path}'>".format(name=self.name, path=self.path)

    def __repr__(self):
        return self.__unicode__()

    @property
    def path(self):
        return Path(self.theme_base_dir) / self.theme_dir_name

    @property
    def template_dirs(self):
        return [
            self.path / 'templates',
            self.path / 'templates' / 'oscar',
        ]
