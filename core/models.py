from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    class Meta:
        abstract = True
