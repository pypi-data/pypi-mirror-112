# last_active

last_active is a Django app to track when a user is last active on a website. The last active time is kept on the database.

It was forked from `django-last-seen`.

The intention is to eventually add weekly active user tracking feature as well.

## Supports Software

- Python: 3.8, 3.9
- Django: 3.2

### Support Policy

For Python, we will always support the latest two minor versions starting with 3.8 and 3.9.

When a new Python minor version is generally available, we will have two releases:

1. a `-final` release for the current major version that includes the latest Python minor
2. a brand new major version that will drop the oldest supported Python version

For Django, at any point in time, there will be a minimum of two or three versions with active support by Django Foundation.

Therefore, this plugin will similarly follow the same road map but with a 2 month delay.

1. when a new Django major version is generally available, the plugin will release a new major version that supports it within 2 months.
2. when a new Django minor version is generally available, the plugin will release a new minor version that supports it within 2 months.
3. when a Django minor version ends its extended support, the plugin will deprecate any versions that support that version 2 months later.

## Installation

1. Add "last_active" to your INSTALLED_APPS setting like this

```
    INSTALLED_APPS = [
        ...
        'last_active',
    ]
```

2. Add 'last_active.middleware.LastActiveMiddleware' to MIDDLEWARE_CLASSES tuple found in your settings file.

3. Run ``python manage.py migrate`` to create the last_active models.

## Settings

**LAST_SEEN_DEFAULT_MODULE**

The default module used on the middleware. The default value is default.

**LAST_SEEN_INTERVAL**

How often is the last seen timestamp updated to the database. The default is 2 hours.