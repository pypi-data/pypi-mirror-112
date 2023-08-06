# django-odoo-auth
[![Upload Python Package](https://github.com/w0rng/django-odoo-auth/actions/workflows/python-publish.yml/badge.svg)](https://github.com/w0rng/django-odoo-auth/actions/workflows/python-publish.yml) 

Custom django auth backend for authorization via odoo

## Quick start
1. install module `pip install django-odoo-auth`  
2. Add odoo_auth to your INSTALLED_APPS setting like this:
```python
INSTALLED_APPS = [
    # ...
    'odoo_auth',
]
```  
3. Add backend to your AUTHENTICATION_BACKENDS setting like this:  
```python
AUTHENTICATION_BACKENDS = (
    # ...
    'odoo_auth.backends.OdooBackend',
)
```  
4. Edit the information to connect to your server Odoo in `settings.py`:  
```python
ODOO_SERVER_URL = 'https://exmaple.com'
ODOO_SERVER_PORT = 443 # this optional
ODOO_SERVER_DBNAME = 'database'
```  
5. Run `python manage.py migrate` to create the odoo_auth models.  
6. For call odoo_auth, use standard authenticate:  
```python
from django.contrib.auth import authenticate
user = authenticate(username='username', password='password')
```
