from django.db import models
from django.conf import settings


class Management(models.Model):
    name = models.CharField("名前", max_length=200)
    tel = models.CharField("電話番号", max_length=200)
    entered = models.DateTimeField("入館", null=True, blank=True)
    exited = models.DateTimeField("退館", null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name
