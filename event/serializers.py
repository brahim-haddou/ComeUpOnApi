from rest_framework import serializers
from event.models import *

from django.contrib.auth.models import User


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    address = PlaceSerializer(read_only=True)
    user = CurrentUserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    place_event = PlaceSerializer()
    activityEvent = ActivitySerializer(many=True)
    
    class Meta:
        model = Event
        fields = '__all__'
        
    def create(self, validated_data):
        place_event = validated_data.pop("place_event")
        activityEvent = validated_data.pop("activityEvent")
        
        event = Event.objects.create(**validated_data)

        Place.objects.create(**place_event)
        for activity in activityEvent:
            Activity.objects.create(activity)
        
        return event


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
