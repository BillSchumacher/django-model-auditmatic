Work in progress
================
- this probably doesn't work well yet.


Usage
-----
- Add django_auditmatic to INSTALLED_APPS.

Example::

    INSTALLED_APPS.append("django_auditmatic")


- Configure which models you want to audit in settings.py

Example::

    AUDITMATIC = {
        "apps": {
            "auth": {
                "User": {"m2m": any},
            }
        }
    }


In this example will only include the User model from the auth app, along with any many-to-many relationships.

- Then run::

    python manage.py install_audit
