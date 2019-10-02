Overview
--------

Django theming provides a way for django sites owners to customize the look
and feel of django sites without having to alter the code of the base site.


Installation
------------

Install using pip:

.. code-block:: sh

    pip install djangotheming

Usage
-----

Add ``'theming'`` to your ``INSTALLED_APPS``.

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'theming',
    ]

Add ``'django.contrib.sites.middleware.CurrentSiteMiddleware'``,
``'theming.middleware.CurrentRequestMiddleware'`` and
``'theming.middleware.CurrentThemeMiddleware'`` to your ``MIDDLEWARE``

Add ``theming.template.loaders.theme.Loader`` to your ``'TEMPLATES['OPTIONS']['loaders']'``

.. code-block:: python

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')]
            ,
            'APP_DIRS': False,
            'OPTIONS': {
                'loaders': [
                    'theming.template.loaders.theme.Loader',
                    'django.template.loaders.app_directories.Loader',
                ],
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]


Set ``'theming.static.storage.ThemeStorage'`` as your ``'STATICFILES_STORAGE'``

.. code-block:: python

    STATICFILES_STORAGE = "theming.static.storage.ThemeStorage"


Add ``'theming.static.finders.ThemeFilesFinder'`` to your ``'STATICFILES_FINDERS'``

.. code-block:: python

    STATICFILES_FINDERS = (
        'theming.static.finders.ThemeFilesFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    )


Finally, Set the ``'THEMING'`` setting to something like.

.. code-block:: python

    #  Theming settings.

    THEMING = {
      'ENABLED': True,
      'DEFAULT': '<theme-name>',
      'DIRS': [

         os.path.join(<absolute-path-to-themes-dir>)

      ],

   }
