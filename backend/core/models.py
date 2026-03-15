import uuid
from django.db import models

class ActiveManager(models.Manager):
    """
    Custom manager to easily filter active records.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True) # This is for soft-deletes and active records, with less redundant code in main apps.


class BaseModel(models.Model):
    """
    Abstract base model that provides common fields to all other models in other apps.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Managers
    objects = models.Manager() # The default manager
    active_data_objects = ActiveManager() # Our custom manager for soft-deletes and active records, with less redundant code in main apps.

    class Meta:
        abstract = True # This tells Django NOT to create a table for BaseModel itself