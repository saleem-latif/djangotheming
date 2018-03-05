"""
Validate thread_locals module of theming.
"""
from functools import partial
from threading import local

import ddt

from django.test import RequestFactory

from test_utils import factories
from test_utils.testcases import TestCase
from theming import thread_locals
from theming.exceptions import MiddlewareNotActivated
from theming.thread_locals import (
    get_current_request,
    get_current_theme,
    get_request_variable,
    get_thread_variable,
    set_current_request,
    set_current_theme,
    set_request_variable,
    set_thread_variable,
)


@ddt.ddt
class ThreadLocalsTests(TestCase):
    """
    Test thread_locals module.
    """

    def setUp(self):
        """
        Save thread locals reference for use in the tests.
        """
        self.thread_locals = thread_locals.__thread_locals__
        self.request = RequestFactory().get('/')
        set_current_request(self.request)

    def tearDown(self):
        """
        clear thread_locals dict.
        """
        self.clear_thread_locals()

    @staticmethod
    def clear_thread_locals():
        """
        Clear thread locals data.
        """
        thread_locals.__thread_locals__ = local()

    def assert_thread_variable(self, key, value, msg=None):
        """
        Assert that current thread contains variable with
        given key and its value is the same as given value.
        """
        self.assertEqual(
            get_thread_variable(key),
            value,
            msg=msg,
        )

    def assert_request_variable(self, key, value, msg=None):
        """
        Assert that current request object contains variable with
        given key and its value is the same as given value.
        """
        self.assertTrue(
            hasattr(self.thread_locals, 'request'), 'Request object not saved in thread data.'
        )
        self.assertEqual(
            get_request_variable(key),
            value,
            msg=msg,
        )

    @ddt.data(
        (lambda: None, 'key', None),
        (partial(set_thread_variable, key='key', value='value'), 'key', 'value'),
        (partial(set_thread_variable, key='key', value=''), 'key', ''),
        (partial(set_thread_variable, key='key', value=None), 'key', None),
    )
    @ddt.unpack
    def test_set_thread_variable(self, test_setup, key, expected):
        """
        Verify set_thread_variable works as expected.
        """
        # Setup test case.
        test_setup()
        self.assert_thread_variable(key, expected)

    @ddt.data(
        (lambda: None, 'key', None),
        (partial(set_thread_variable, key='key', value='value'), 'key', 'value'),
        (partial(set_thread_variable, key='key', value=''), 'key', ''),
        (partial(set_thread_variable, key='key', value=None), 'key', None),
    )
    @ddt.unpack
    def test_get_thread_variable(self, test_setup, key, expected):
        """
        Verify get_thread_variable works as expected.
        """
        # Setup test case.
        test_setup()

        self.assertEqual(
            get_thread_variable(key),
            expected,
        )

    @ddt.data(
        (lambda: None, 'key', None),
        (partial(set_request_variable, key='key', value='value'), 'key', 'value'),
        (partial(set_request_variable, key='key', value=''), 'key', ''),
        (partial(set_request_variable, key='key', value=None), 'key', None),
    )
    @ddt.unpack
    def test_set_request_variable(self, test_setup, key, expected):
        """
        Verify set_request_variable works as expected.
        """
        # Setup test case.
        test_setup()

        self.assert_request_variable(key, expected)

    def test_set_request_variable_raises_exception(self):  # pylint: disable=invalid-name
        """
        Verify set_request_variable raises exception if request object is not saved in local thread.
        """
        # clear thread locals to cause the error
        self.clear_thread_locals()

        with self.assertRaises(MiddlewareNotActivated):
            set_request_variable('theme-name', 'test-theme')

    @ddt.data(
        (lambda: None, 'key', None),
        (partial(set_request_variable, key='key', value='value'), 'key', 'value'),
        (partial(set_request_variable, key='key', value=''), 'key', ''),
        (partial(set_request_variable, key='key', value=None), 'key', None),
    )
    @ddt.unpack
    def test_get_request_variable(self, test_setup, key, expected):
        """
        Verify get_request_variable works as expected.
        """
        # Setup test case.
        test_setup()

        self.assertEqual(
            get_request_variable(key),
            expected,
        )

    def test_get_request_variable_raises_exception(self):  # pylint: disable=invalid-name
        """
        Verify get_request_variable raises exception if request object is not saved in local thread.
        """
        # clear thread locals to cause the error
        self.clear_thread_locals()

        with self.assertRaises(MiddlewareNotActivated):
            get_request_variable('theme-name', 'test-theme')

    def test_set_current_request(self):
        """
        Verify set_current_request works as expected.
        """
        set_current_request(self.request)
        self.assert_thread_variable('request', self.request)

    def test_get_current_request(self):
        """
        Verify get_current_request works as expected.
        """
        set_current_request(self.request)

        self.assertEqual(
            get_current_request(),
            self.request,
        )

    def test_set_current_theme(self):
        """
        Verify set_current_theme works as expected.
        """
        theme = factories.ThemeFactory()
        set_current_theme(theme)
        self.assert_request_variable('theme', theme)

    def test_get_current_theme(self):
        """
        Verify get_current_theme works as expected.
        """
        theme = factories.ThemeFactory()
        set_current_theme(theme)

        self.assertEqual(
            get_current_theme(),
            theme,
        )
