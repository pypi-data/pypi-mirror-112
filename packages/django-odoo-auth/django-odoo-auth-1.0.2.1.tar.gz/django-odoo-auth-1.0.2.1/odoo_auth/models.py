from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class OdooUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    odoo_id = models.BigIntegerField(primary_key=True)
