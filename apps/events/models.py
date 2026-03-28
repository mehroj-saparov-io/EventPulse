from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Event(models.Model):
    ONLINE = 'ONLINE'
    OFFLINE = 'OFFLINE'
    EVENT_TYPES = [
        (ONLINE, 'Online'),
        (OFFLINE, 'Offline'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.CharField(max_length=7, choices=EVENT_TYPES)
    location = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # end_time < start_time check
        if self.end_time < self.start_time:
            raise ValidationError("End time cannot be before start time")

        # location required for OFFLINE
        if self.event_type == self.OFFLINE and not self.location:
            raise ValidationError("Offline events must have a location")

    def __str__(self):
        return self.title