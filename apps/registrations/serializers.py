from rest_framework import serializers
from .models import Registration

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, attrs):
        event = attrs['event']
        user = self.context['request'].user

        # Check if user already registered
        if Registration.objects.filter(user=user, event=event, status='REGISTERED').exists():
            raise serializers.ValidationError("You are already registered for this event")

        # Check event capacity
        registered_count = event.registrations.filter(status='REGISTERED').count()
        if registered_count >= event.capacity:
            raise serializers.ValidationError("Event capacity exceeded")

        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)