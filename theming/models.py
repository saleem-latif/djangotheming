from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from path import Path

import theming


class Theme(models.Model):
    """
    This is where the information about the site's theme gets stored to the db.

    Fields:
        site (ForeignKey): Foreign Key field pointing to django Site model
        theme_dir_name (CharField): Contains directory name for any site's theme (e.g. 'red-theme')
    """
    site = models.OneToOneField(Site, related_name='theme', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __eq__(self, other):
        """
        Returns True if given theme is same as the self
        Args:
            other: Theme object to compare with self

        Returns:
            (bool) True if two themes are the same else False
        """
        return (self.name, self.path) == (other.name, other.path)

    def __hash__(self):
        return hash((self.name, self.path))

    def __unicode__(self):
        return u"<Theme: {name} at '{path}'>".format(name=self.name, path=self.path)

    def __repr__(self):
        return self.__unicode__()

    @property
    def base_dir(self):
        # TODO: handle theme not found
        return Path(theming.get_base_dir(str(self.name)))

    @property
    def path(self):
        return self.base_dir / self.name

    @property
    def template_dirs(self):
        return [
            self.path / 'templates',
        ]

    @staticmethod
    def get_theme(site):
        """
        Get SiteTheme object for given site, returns default site theme if it can not
        find a theme for the given site and `DEFAULT_SITE_THEME` setting has a proper value.

        Args:
            site (django.contrib.sites.models.Site): site object related to the current site.

        Returns:
            SiteTheme object for given site or a default site set by `DEFAULT_SITE_THEME`
        """
        if not site:
            return None

        theme = None

        try:
            theme = site.theme
        except Theme.DoesNotExist:
            pass

        if (not theme) and settings.THEMING.get('DEFAULT', None):
            theme = Theme(site=site, name=settings.THEMING['DEFAULT'])

        return theme
