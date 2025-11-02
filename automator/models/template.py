from django.contrib.auth.models import User
from django.db import models
from .base import BaseModel

class Template(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='templates')
 
 
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()



    class Meta:
        verbose_name="Template"
        verbose_name_plural="Templates"

        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"], 
                condition=models.Q(deleted_at__isnull=True),
                name="unique_user_template_name"
            )
        ]

        db_table="templates"

        indexes = [
            models.Index(fields=["user", "title", "name"])
        ]

    def __str__(self):
        return f"{self.name} ({self.user.username})" 