from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from event.models import *

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    username = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return email
    
    def validate_password1(self, password):
        return get_adapter().clean_password(password)
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data
    
    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    address = PlaceSerializer()
    user = CurrentUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        image = validated_data.pop('image')
        address = validated_data.pop("address")
    
        place = Place.objects.create(**address)
    
        profile = Profile.objects.create(image=image, address=place, **validated_data)
        return profile


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
        
        event = Event.objects.create(image=image, place_event=place, **validated_data)
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
