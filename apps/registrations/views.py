from rest_framework import generics, permissions
from .models import Registration
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.events.models import Event
from django.db.models import Count
from .permissions import IsAdminUser

class EventStatsView(APIView):
    permission_classes = [IsAdminUser]
class RegistrationCreateView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegistrationCancelView(generics.UpdateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user, status='REGISTERED')

    def perform_update(self, serializer):
        serializer.save(status='CANCELLED')

# Statistics endpoints
class EventStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        events = Event.objects.annotate(
            registered_count=Count('registrations', filter=models.Q(registrations__status='REGISTERED'))
        ).order_by('-registered_count')

        data = []
        for event in events:
            data.append({
                'id': event.id,
                'title': event.title,
                'registered_count': event.registered_count,
                'available_seats': max(event.capacity - event.registered_count, 0)
            })

        top5 = data[:5]
        return Response({'all_events': data, 'top5': top5})