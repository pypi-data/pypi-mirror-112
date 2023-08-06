from xmlrpc.client import ServerProxy as XmlrpcServerProxy

from django.contrib.auth.backends import BaseBackend

from . import settings
from .models import OdooUser, User


class OdooBackend(BaseBackend):
    def __init__(self):
        url = settings.ODOO_SERVER_URL
        if settings.ODOO_SERVER_PORT is not None:
            url += f':{settings.ODOO_SERVER_PORT}'
        url_login = f'{url}/xmlrpc/2/common'
        self.ODOO_SOCK_COMMON = XmlrpcServerProxy(url_login)

    def authenticate(self, request, username=None, password=None):
        user = User.objects.filter(username=username).first()
        if user:
            return user if user.check_password(password) else None

        user_uid = self.ODOO_SOCK_COMMON.authenticate(
            settings.ODOO_SERVER_DBNAME,
            username,
            password,
            {},
        )
        if user_uid is None:
            return None

        user.set_password(password)
        user.save()

        OdooUser.objects.create(odoo_id=user_uid, user=user)
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
