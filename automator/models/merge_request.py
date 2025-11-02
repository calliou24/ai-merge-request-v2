from django.contrib.auth.models import User
from django.db import models
from .base import BaseModel
from .project import Project

class MergeRequest(BaseModel):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='merge_requests')
    project=models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name='merge_requests')

    merge_request_id=models.IntegerField(unique=True)
    title=models.TextField()
    description=models.TextField()
    project_name=models.CharField(max_length=255)

    class Meta:
        verbose_name='Merge Request'
        verbose_name_plural='Merges Requests'

        db_table='merge_request'

        indexes = [
            models.Index(fields=["user", 'merge_request_id'])
        ]
    
    def __str__(self):
        return f"{self.merge_request_id} ({self.user.username})"
        


   