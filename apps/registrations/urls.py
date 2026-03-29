from django.urls import path
from .views import RegistrationCreateView, RegistrationCancelView, EventStatsView

urlpatterns = [
    path('register/', RegistrationCreateView.as_view(), name='register'),
    path('cancel/<int:pk>/', RegistrationCancelView.as_view(), name='cancel-registration'),
    path('stats/', EventStatsView.as_view(), name='event-stats'),
]