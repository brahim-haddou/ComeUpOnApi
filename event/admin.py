from django.contrib import admin
from event.models import (Place, Profile, Follower, Activity,
                          Event, Participant, Message, ActivityEvent)

# Register your models here.
admin.site.register(Place)
admin.site.register(Profile)
admin.site.register(Follower)
admin.site.register(Activity)
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Message)
admin.site.register(ActivityEvent)