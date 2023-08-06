from .interfaces import *
from django.db import models
from .interfaces import *


class CreatedUpdatedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
