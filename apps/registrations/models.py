from django.db import models
from django.conf import settings
from apps.events.models import Event
from django.core.exceptions import ValidationError

class Registration(models.Model):
    REGISTERED = 'REGISTERED'
    CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [
        (REGISTERED, 'Registered'),
        (CANCELLED, 'Cancelled')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=REGISTERED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'event')  # bitta user bitta eventga faqat 1 marta

    def clean(self):
        if self.status == self.REGISTERED and self.event.capacity <= self.event.registrations.filter(status=self.REGISTERED).count():
            raise ValidationError("Event capacity exceeded")

    def __str__(self):
        return f"{self.user.email} - {self.event.title} ({self.status})"