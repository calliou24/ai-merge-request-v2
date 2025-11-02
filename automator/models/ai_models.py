
from django.db import models
from .base import BaseModel

class AiProviderStatusChoises(models.TextChoices):
    ACTIVE = 'ACTIVE'
    DISABLED = 'DISABLED'

class AIProviderNameCoices(models.TextChoices):
    OPEN_ROUTER = 'open_router'
    CEREBRAS = 'cerebras'

class AiProvider(BaseModel):
    name = models.CharField(choices=AIProviderNameCoices.choices)
    status = models.CharField(choices=AiProviderStatusChoises.choices, default=AiProviderStatusChoises.ACTIVE)

    class Meta: 
        verbose_name = 'AI Provider' 
        verbose_name_plural = 'AI Providers'
        db_table = 'ai_provider'

        indexes = [ 
            models.Index(
                fields=['name', 'status'],
                name='ai_provider_name_status'
            )
        ]

    def __str__(self):
        return f"({self.name}) ({self.status})"


class AiModel(BaseModel):
    provider=  models.ForeignKey(to=AiProvider, on_delete=models.CASCADE)
    name = models.CharField()


    class Meta:
        verbose_name = 'Ai Model'
        verbose_name_plural = 'Ai Models'
        db_table = 'ai_model'

        indexes = [
            models.Index(
                fields=['name'],
                name='ai_model_name'
            )
        ]

    def __str__(self):
        return f"({self.name}) ({self.provider.name})"