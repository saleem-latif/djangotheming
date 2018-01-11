"""
Module to contain model definitions for theming app.
"""

from path import Path

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

import theming


class Theme(models.Model):
    """
    Django ORM model for Theme db table.

    Fields:
        site (ForeignKey): Foreign Key field pointing to django Site model
        theme_dir_name (CharField): Contains directory name for any site's theme (e.g. 'red-theme')
    """

    site = models.OneToOneField(Site, related_name='theme', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __eq__(self, other):
        """
        Return True if given theme is same as the self.

        Arguments:
            other: Theme object to compare with self

        Returns:
            (bool) True if two themes are the same else False
        """
        return (self.name, self.path) == (other.name, other.path)

    def __hash__(self):
        """
        Return unique hash for the theme.
        """
        return hash((self.name, self.path))

    def __str__(self):
        """
        Return unique readable string for the theme.
        """
        return u"<Theme: {name} at '{path}'>".format(name=self.name, path=self.path)

    def __repr__(self):
        """
        Return unique readable string for the theme.
        """
        return self.__str__()

    @property
    def base_dir(self):
        """
        Return base directory path for the theme.
        """
        # TODO: handle theme not found
        return Path(theming.get_base_dir(str(self.name)))

    @property
    def path(self):
        """
        Return full directory path for the theme.
        """
        return self.base_dir / self.name

    @property
    def template_dirs(self):
        """
        Return list of all template directories of the theme.
        """
        return [
            self.path / 'templates',
        ]

    @staticmethod
    def get_theme(site):
        """
        Return SiteTheme object for given site.

        Return default site theme if theme for the given site can not be found
        and `DEFAULT_SITE_THEME` setting has a proper value.

        Arguments:
            site (django.contrib.sites.models.Site): site object related to the current site.

        Returns:
            SiteTheme object for given site or a default site set by `DEFAULT_SITE_THEME`
        """
        try:
            return site.theme
        except ObjectDoesNotExist:
            if settings.THEMING.get('DEFAULT', None):
                return Theme(site=site, name=settings.THEMING['DEFAULT'])
            return None
