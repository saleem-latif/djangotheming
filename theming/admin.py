"""
Module containing admin interfaces for the theming app.
"""
from __future__ import absolute_import

from django.contrib import admin

from .models import Theme


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    """
    Admin UI definitions for `Theme` model.
    """

    list_display = ('site', 'name')
    search_fields = ('site__domain', 'name')
