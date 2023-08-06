from django.db import models


class ExpiredToken(models.Model):

    token = models.CharField(max_length=1000, null=False)
    datetime = models.DateTimeField(auto_now_add=True)
