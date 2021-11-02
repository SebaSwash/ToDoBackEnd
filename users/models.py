from django.utils import timezone
from django.db import models

# Modelo de Usuario
class User(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=300)
    institution = models.CharField(max_length=300, null=True)
    password_recovery_token = models.CharField(max_length=300, default=None)
    last_password_recovery_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'User'

