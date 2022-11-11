from django.db import models
from user_service.models import User
from . import QueryPriorityTypes, QueryStatus
from django.db.models import JSONField
from django.core.serializers.json import DjangoJSONEncoder, Serializer as JsonSerializer

# Create your models here.


class Serializer(JsonSerializer):
    def _init_options(self):
        super()._init_options()
        self.json_kwargs["cls"] = CustomJsonEncoder


class CustomJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        return super().default(obj)

class Message(models.Model):
    message_text = models.TextField(null=True)
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="messages",
        on_delete=models.SET_NULL,
    )
    staff = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="assigned_messages",
        on_delete=models.SET_NULL,
    )
    priority = models.CharField(
        max_length = 10, choices = QueryPriorityTypes.CHOICES, default=QueryPriorityTypes.HIGH
    )
    status = models.CharField(
        max_length = 20, choices = QueryStatus.CHOICES, default=QueryStatus.QUERY_RECEIVED
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    private_metadata = JSONField(
        blank=True, null=True, default=dict, encoder=CustomJsonEncoder
    )
    metadata = JSONField(blank=True, null=True, default=dict, encoder=CustomJsonEncoder)

    def __str__(self):
        return self.message_text

