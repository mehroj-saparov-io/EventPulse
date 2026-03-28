from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def validate(self, data):
        if data['end_time'] < data['start_time']:
            raise serializers.ValidationError("End time cannot be before start time")

        if data['event_type'] == Event.OFFLINE and not data.get('location'):
            raise serializers.ValidationError("Offline events must have a location")

        if data['capacity'] < 0:
            raise serializers.ValidationError("Capacity cannot be negative")

        return data