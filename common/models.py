from django.db import models
import uuid
from django.utils import timezone


class BaseModel(models.Model):
    """
    Abstract base model that provides timestamp fields.
    """

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
