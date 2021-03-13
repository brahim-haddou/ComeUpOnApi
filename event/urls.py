from django.urls import include, path
from event.views import *

urlpatterns = [
    
    path('Place/', PlaceView.as_view(), name="Place"),  # get all Place, post add Place
    path('Place/<int:ID>/', place_details),  # get, put, delete
    
    path('Profile/', profile),  # get all profiles, post add profile
    path('Profile/me/', ProfileView.as_view(), name='Profile'),  # get, put, delete
    
    path('Activity/', ActivityView.as_view(), name='Activity'),
    path('Activity/<int:ID>/', activity_details),
    
    path('Event/', EventView.as_view(), name='Event'),
    path('Event/<int:ID>/', event_details),
    path('Event/<int:event_id>/Participant/<int:state>/', ParticipantView.as_view(), name='Participant'),
    path('Event/<int:event_id>/Participant/', ParticipantView.as_view(), name='Participant'),
    path('Event/<int:event_id>/Participant/State/', ParticipantStateView.as_view(), name='ParticipantState'),
    
    path('MeFollowing/', MeFollowingView.as_view(), name='MeFollowing'),
    path('MyFollowers/', MyFollowersView.as_view(), name='MyFollowers'),
    path('AmIFollowing/<int:profile_id>/', AmIFollowingView.as_view(), name='AmIFollowing'),
    
    path('Participant/<int:profile_id>/Follow/', FollowParticipantView.as_view(), name='FollowParticipant'),
    # path('Participant/', participant),
    # path('Participant/<int:ID>/', participant_details),
    #
    # path('Message/', message),
    # path('Message/<int:ID>/', message_details),
]
