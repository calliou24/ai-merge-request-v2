
from django.contrib.auth.models import User
from django.db import models
from .base import BaseModel


class PAT(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pats")
    
    #
    name=models.CharField(max_length=255)
    encrypted_pat=models.TextField()
    is_active=models.BooleanField(default=True)


    class Meta:
        verbose_name="Personal Access Token"
        verbose_name_plural="Personal Access Tokens"
        
        db_table = "pat"
        
        constraints = [ 
            models.UniqueConstraint(
                fields=["user", "name"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_user_pat"
            )
        ]

        indexes = [
            models.Index(fields=["name"])
        ]
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"


    def activate(self):
        self.is_active=True
        self.save()

    def deactivate(self):
        self.is_active= False
        self.save()