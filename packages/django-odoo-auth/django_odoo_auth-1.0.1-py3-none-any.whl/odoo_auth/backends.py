import xmlrpc.client

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from . import settings


User = get_user_model()


class OdooBackend(BaseBackend):
    def __init__(self):
        url = settings.ODOO_SERVER_URL
        if settings.ODOO_SERVER_PORT is None:
            url += f':{settings.ODOO_SERVER_PORT}'
        url_login = f'{url}/xmlrpc/2/common'
        self.ODOO_SOCK_COMMON = xmlrpc.client.ServerProxy(url_login)

    def authenticate(self, request, username=None, password=None):
        user_uid = self.ODOO_SOCK_COMMON.authenticate(
            settings.ODOO_SERVER_DBNAME,
            username,
            password,
            {},
        )
        if user_uid is None:
            return None
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            return user
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
