from django.urls import path
from event.views import *

urlpatterns = [
    path('Place/', PlaceView.as_view(), name="Place"),  # get all Place, post add Place
    path('Place/<int:ID>/', place_details),  # get, put, delete
    
    path('Profile/', profile),  # get all profiles, post add profile
    path('Profile/<int:ID>/', profile_details),  # get, put, delete
    
    path('Profile/<int:id_user>/Followers/', follower),  # get followers, post follow, delete unfollow
    path('Profile/<int:id_user>/Following/', following),  # get following
    
    path('Activity/', ActivityView.as_view(), name='Activity'),
    path('Activity/<int:ID>/', activity_details),
    
    path('Event/', EventView.as_view(), name='Event'),
    path('Event/<int:ID>/', event_details),
    path('Event/<int:event_id>/Participant/', participant),
    
    path('Participant/', participant),
    path('Participant/<int:ID>/', participant_details),
    
    path('Message/', message),
    path('Message/<int:ID>/', message_details),
]
