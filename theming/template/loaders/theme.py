"""
Wrapper for loading templates from "templates" directories for themes.
"""

from django.template.loaders.filesystem import Loader as FilesystemLoader

from theming import get_themes
from theming.thread_locals import get_current_request, get_current_theme


class Loader(FilesystemLoader):
    """
    Theming aware template loader.
    """
    def get_dirs(self):
        """
        Return all template directories including theme template directories.

        Returns:
            (list): A list containing template directories.
        """
        # TODO: Cache result for faster performance
        dirs = super(Loader, self).get_dirs()
        theme_dirs = []

        if get_current_request():
            # If the template is being loaded in a request, prepend the current theme's template directories
            # so the theme's templates take precedence.
            theme = get_current_theme()

            if theme:
                theme_dirs = theme.template_dirs
        else:
            # If we are outside of a request, we should load all directories for all themes.
            for theme in get_themes():
                theme_dirs.extend(
                    theme.template_dirs
                )

        return theme_dirs + dirs
