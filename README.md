
Work in progress - this probably doesn't work well yet.
===

Usage
---
Add django_auditmatic to INSTALLED_APPS.

```
INSTALLED_APPS.append("django_auditmatic")
```

Configure which models you want to audit in settings.py

```python
AUDITMATIC = {
    "apps": {
        "auth": {
            "User": {"m2m": any},
        }
    }
}
```

For example will only include the User model from the auth app, along with any many-to-many relationships.

Then run:

```shell
python manage.py install_audit
```