"""
Test theming middleware.
"""

from django.test import RequestFactory

from test_utils.testcases import TestCase
from test_utils import factories
from theming.middleware import CurrentRequestMiddleware, CurrentThemeMiddleware
from theming.thread_locals import get_current_request, get_current_theme


class CurrentRequestMiddlewareTest(TestCase):
    """
    Verify that CurrentRequestMiddleware works as expected.
    """
    def setUp(self):
        """
        Setup middleware and request instances.
        """
        self.middleware = CurrentRequestMiddleware()
        self.request = RequestFactory().get('/')

    def test_process_request(self):
        """
        Verify that `process_request` of CurrentRequestMiddleware saves request object in
        thread data.
        """
        # Verify that request is not previously set.
        self.assertIsNone(get_current_request())

        self.middleware.process_request(request=self.request)
        self.assertEqual(
            get_current_request(),
            self.request
        )


class CurrentThemeMiddlewareTest(TestCase):
    """
    Verify that CurrentThemeMiddleware works as expected.
    """
    def setUp(self):
        """
        Setup middleware and request instances.
        """
        self.middleware = CurrentThemeMiddleware()
        self.request = RequestFactory().get('/')
        self.theme = factories.ThemeFactory()
        self.request.site = self.theme.site

    def test_process_request(self):
        """
        Verify that `process_request` of CurrentThemeMiddleware associates theme with the current request.
        """
        # Verify that theme is not previously set.
        self.assertIsNone(get_current_theme())

        self.middleware.process_request(request=self.request)
        self.assertEqual(
            get_current_theme(),
            self.theme
        )
