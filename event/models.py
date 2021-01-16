from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Place(models.Model):
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    lat = models.FloatField()
    lan = models.FloatField()

    def __str__(self):
        return self.address


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/profile/")
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    address = models.ForeignKey(Place, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username


class Follower(models.Model):
    user_id = models.OneToOneField("Profile", related_name="following", on_delete=models.CASCADE)
    follow = models.ManyToManyField("Profile", related_name="followers")

    def __str__(self):
        return self.user_id.user.username + " follow"


class Activity(models.Model):
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=80)
    image = models.ImageField(upload_to="images/activity/")
    number_Activity = models.PositiveIntegerField()
    number_Participant = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Event(models.Model):
    owner = models.ForeignKey("Profile", related_name="owner", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/event/")
    description = models.CharField(max_length=300)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    place_event = models.ForeignKey("Place", on_delete=models.CASCADE)
    activityEvent = models.ManyToManyField("Activity", related_name="activityEvent")
    
    def __str__(self):
        return self.title


class Participant(models.Model):
    event_participant_id = models.ForeignKey("Event", on_delete=models.CASCADE)
    user_participant_id = models.ForeignKey("Profile", on_delete=models.CASCADE)
    stat = models.BooleanField(default=False)


class Message(models.Model):
    event_Message_id = models.ForeignKey("Event", on_delete=models.CASCADE)
    user_Message_id = models.ForeignKey("Profile", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    time = models.DateTimeField()
