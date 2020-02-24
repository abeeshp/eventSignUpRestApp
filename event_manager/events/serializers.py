from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import Event, Registration


class EventSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['start_time'] <= timezone.now():
            raise serializers.ValidationError("Event startTime cannot be in the past")
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Event startTime must be before endTime")
        return data

    class Meta:
        model = Event
        fields = ('id', 'name', 'location', 'start_time', 'end_time', 'description')

        validators = [
            UniqueTogetherValidator(
                queryset=Event.objects.all(),
                fields=['name', 'location', 'start_time', 'end_time'],
                message="There's already an event scheduled with same name/location/star and end times"
            ),
            UniqueValidator(
                queryset=Event.objects.all(),
                message="There's already an event scheduled with same name, try adding with a different name"
            ),
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('id', 'name', 'email', 'event')

        validators = [
            UniqueTogetherValidator(
                queryset=Registration.objects.all(),
                fields=['event', 'email'],
                message="This email is already registered for the event"
            )
        ]
