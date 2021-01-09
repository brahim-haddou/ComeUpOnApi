from pprint import pprint

from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from event.models import *

from drf_extra_fields.fields import Base64ImageField

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
    image = Base64ImageField()
    
    class Meta:
        model = Activity
        fields = '__all__'
    
    def create(self, validated_data):
        image = validated_data.pop('image')
        
        return Activity.objects.create(image=image, **validated_data)


class EventSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    place_event = PlaceSerializer()
    activityEvent = ActivitySerializer(many=True)
    owner = ProfileSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(), source='owner', write_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'
    
    def create(self, validated_data):
        image = validated_data.pop('image')
        place_event = validated_data.pop("place_event")
        activityEvent = validated_data.pop("activityEvent")
        
        place = Place.objects.create(**place_event)
        
        activities = []
        for activity in activityEvent:
            activities.append(Activity.objects.create(**activity))

        event = Event.objects.create(image=image, place_event=place,  **validated_data)
        event.activityEvent.add(*activities)
      
        return event


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
