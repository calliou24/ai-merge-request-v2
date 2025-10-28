from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

# BaseModel
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
       abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()
    
    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def restore(self):
        self.deleted_at = None
        self.save()


#
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
#
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

#
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
        
