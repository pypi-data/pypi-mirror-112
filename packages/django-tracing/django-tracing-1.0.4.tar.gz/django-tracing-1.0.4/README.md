Tracing
=====

Tracing is a Django app to trace changes in models.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "tracing" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'tracing',
    ]

3. Run ``python manage.py migrate`` to create the tracing migrations.

4. Continue