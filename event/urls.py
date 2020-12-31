from django.urls import path
from event.views import *

urlpatterns = [
    path('Place/', place),  # get all Place, post add Place
    path('Place/<int:ID>/', place_details),  # get, put, delete
    
    path('Profile/', profile),  # get all profiles, post add profile
    path('Profile/<int:ID>/', profile_details),  # get, put, delete
    
    path('Profile/<int:id_user>/Followers/', follower),  # get followers, post follow, delete unfollow
    path('Profile/<int:id_user>/Following/', following),  # get following
    
    path('Activity/', activity),
    path('Activity/<int:ID>/', activity_details),
    
    path('Event/', event),
    path('Event/<int:ID>/', event_details),
    
    path('Participant/', participant),
    path('Participant/<int:ID>/', participant_details),
    
    path('Message/', message),
    path('Message/<int:ID>/', message_details),
]
