from django.contrib.auth.models import User
from django.db import models
from .base import BaseModel


class Project(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    name=models.CharField(max_length=255)
    project_id=models.IntegerField()
    

    class Meta:
        verbose_name='Project'
        verbose_name_plural="Projects"

        db_table='project'

        constraints = [
            models.UniqueConstraint(
                fields=["user", "project_id"], 
                condition=models.Q(deleted_at__isnull=True),
                name="unique_user_project_name"
            )
        ]

        indexes = [
            models.Index(fields=["name", "project_id"])
        ]

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
