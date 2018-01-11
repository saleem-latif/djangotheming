"""
Static file finders for Django.
https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-STATICFILES_FINDERS
Yes, this interface is private and undocumented, but we need to access it anyway.
"""
import os
from collections import OrderedDict

from django.conf import settings
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseFinder
from django.core.checks import Error
from django.utils import six

import theming
from theming.static.storage import ThemeStorage


class ThemeFilesFinder(BaseFinder):
    """
    A static files finder that looks in the directory of each theme as
    specified in the source_dir attribute.
    """
    storage_class = ThemeStorage
    source_dir = 'static'

    def __init__(self, *args, **kwargs):
        # The list of themes that are handled
        self.themes = []
        # Mapping of theme names to storage instances
        self.storages = OrderedDict()

        if theming.is_enabled():
            themes = theming.get_themes()
            for theme in themes:
                theme_storage = self.storage_class(
                    os.path.join(theme.path, self.source_dir),
                    prefix=theme.name,
                )

                self.storages[theme.name] = theme_storage
                if theme.name not in self.themes:
                    self.themes.append(theme.name)

        super(ThemeFilesFinder, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = []
        if 'DIRS' not in settings.THEMING:
            errors.append(Error(
                'The THEMING["DIRS"] setting must be populated.',
                id='theming.static.E001',
            ))
        elif not isinstance(settings.THEMING['DIRS'], (list, tuple)):
            errors.append(Error(
                'The THEMING["DIRS"] setting is not a tuple or list.',
                hint='Perhaps you forgot a trailing comma?',
                id='theming.static.E002',
            ))
        elif not all([isinstance(theme_dir, str) for theme_dir in settings.THEMING['DIRS']]):
            errors.append(Error(
                'THEMING["DIRS"] must contain only strings.',
                id='theming.static.E003',
            ))
        elif not all([theme_dir.startswith("/") for theme_dir in settings.THEMING['DIRS']]):
            errors.append(Error(
                'THEMING["DIRS"] must contain only absolute paths to themes dirs.',
                id='theming.static.E004',
            ))
        elif not all([os.path.isdir(theme_dir) for theme_dir in settings.THEMING['DIRS']]):
            errors.append(Error(
                'THEMING["DIRS"] must contain valid paths.',
                id='theming.static.E005',
            ))
        return errors

    def list(self, ignore_patterns):
        """
        List all files in all theme storages.
        """
        for storage in six.itervalues(self.storages):
            if storage.exists(''):  # check if storage location exists
                for path in utils.get_files(storage, ignore_patterns):
                    yield path, storage

    def find(self, path, all=False):  # pylint: disable=redefined-builtin
        """
        Looks for files in the theme directories.
        """
        matches = []
        theme_dir = path.split("/", 1)[0]

        themes = {t.name: t for t in theming.get_themes()}
        # if path is prefixed by theme name then search in the corresponding storage other wise search all storages.
        if theme_dir in themes:
            theme = themes[theme_dir]
            path = "/".join(path.split("/")[1:])
            match = self.find_in_theme(theme.name, path)
            if match:
                if not all:
                    return match
                matches.append(match)
        return matches

    def find_in_theme(self, theme_name, path):
        """
        Find a requested static file in an theme's static locations.
        """
        storage = self.storages.get(theme_name, None)
        if storage:
            # only try to find a file if the source dir actually exists
            if storage.exists(path):
                matched_path = storage.path(path)
                if matched_path:
                    return matched_path
        return None
