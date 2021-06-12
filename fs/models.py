from django.contrib.auth.models import Permission, User
from django.db import models


class Us(models.Model):
    username = models.CharField(max_length=6)
    em = models.CharField(max_length=30)
    cn = models.CharField(max_length=20)
    rl = models.CharField(max_length=20)
    ic = models.FileField(upload_to='media/')
    is_ad = models.BooleanField(default=False)
    pe = models.CharField(max_length=3)
    is_act = models.BooleanField(default=False)
    otp = models.IntegerField(default=0000)
    password = models.CharField(max_length=20)
    fn = models.CharField(max_length=20)
    ln = models.CharField(max_length=20)

class sug(models.Model):
    EC = models.CharField(max_length=50)
    EN = models.CharField(max_length=500)
    ER = models.CharField(max_length=500)
    S = models.CharField(max_length=500)