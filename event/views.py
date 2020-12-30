from pprint import pprint

from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser

from event.serializers import *
from event.models import *


@csrf_exempt
def place(request):
    if request.method == "GET":
        data = Place.objects.all()
        serializer = PlaceSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = PlaceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def place_details(request, ID):
    try:
        instance = Place.objects.get(id=ID)
    except Place.DoesNotExist as e:
        return JsonResponse({"error": "Given Place object not found."}, status=404)
    
    if request.method == "GET":
        serializer = PlaceSerializer(instance)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = PlaceSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        instance.delete()
        return JsonResponse(status=204)


@csrf_exempt
def profile(request):
    if request.method == "GET":
        data = Profile.objects.all()
        serializer = ProfileSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def profile_details(request, ID):
    try:
        instance = Profile.objects.get(id=ID)
    except Profile.DoesNotExist as e:
        return JsonResponse({"error": "Given Place object not found."}, status=404)
    
    if request.method == "GET":
        serializer = ProfileSerializer(instance)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        instance.delete()
        return JsonResponse(status=204)


@csrf_exempt
def follower(request, id_user):
    try:
        instance = Follower.objects.get(user_id=id_user)
    except Follower.DoesNotExist as e:
        return JsonResponse({"error": "Given Place object not found."}, status=404)
    
    if request.method == "GET":
        data = Follower.objects.filter(followers__id=id_user).only('user_id')
        data = Profile.objects.filter(pk__in=data.values_list('id', flat=True))
        serializer = ProfileSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        instance.followers.add(data['user'])
        serializer = FollowerSerializer(instance)
        return JsonResponse(serializer.data, status=200)
    elif request.method == "DELETE":
        data = JSONParser().parse(request)
        instance.followers.remove(data['user'])
        serializer = FollowerSerializer(instance)
        return JsonResponse(serializer.data, status=200)


@csrf_exempt
def following(request, id_user):
    if request.method == "GET":
        data = Follower.objects.all().filter(user_id=id_user)
        data = Profile.objects.filter(pk__in=data.values_list('followers__id', flat=True))
        serializer = ProfileSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def activity(request):
    if request.method == "GET":
        data = Activity.objects.all()
        serializer = ActivitySerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ActivitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def activity_details(request, ID):
    try:
        instance = Activity.objects.get(id=ID)
    except Activity.DoesNotExist as e:
        return JsonResponse({"error": "Given Place object not found."}, status=404)
    
    if request.method == "GET":
        serializer = ActivitySerializer(instance)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = ActivitySerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        instance.delete()
        return JsonResponse(status=204)


@csrf_exempt
def event(request):
    if request.method == "GET":
        data = Event.objects.all()
        serializer = EventSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def event_details(request, ID):
    try:
        instance = Event.objects.get(id=ID)
    except Event.DoesNotExist as e:
        return JsonResponse({"error": "Given Place object not found."}, status=404)
    
    if request.method == "GET":
        serializer = EventSerializer(instance)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = EventSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        instance.delete()
        return JsonResponse(status=204)


@csrf_exempt
def participant(request):
    if request.method == "GET":
        data = Participant.objects.all()
        serializer = ParticipantSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ParticipantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def participant_details(request, ID):
    try:
        instance = Participant.objects.get(id=ID)
    except Participant.DoesNotExist as e:
        return JsonResponse({"error": "Given Place object not found."}, status=404)
    
    if request.method == "GET":
        serializer = ParticipantSerializer(instance)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = ParticipantSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        instance.delete()
        return JsonResponse(status=204)


@csrf_exempt
def message(request):
    if request.method == "GET":
        data = Message.objects.all()
        serializer = MessageSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def message_details(request, ID):
    try:
        instance = Message.objects.get(id=ID)
    except Message.DoesNotExist as e:
        return JsonResponse({"error": "Given Place object not found."}, status=404)
    
    if request.method == "GET":
        serializer = MessageSerializer(instance)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.erros, status=400)
    elif request.method == "DELETE":
        instance.delete()
        return JsonResponse(status=204)


@csrf_exempt
def activityEvent(request):
    if request.method == "GET":
        data = ActivityEvent.objects.all()
        serializer = ActivityEventSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ActivityEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def activityEvent_details(request, ID):
    try:
        instance = ActivityEvent.objects.get(id=ID)
    except ActivityEvent.DoesNotExist as e:
        return JsonResponse({"error": "Given Place object not found."}, status=404)
    
    if request.method == "GET":
        serializer = ActivityEventSerializer(instance)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = ActivityEventSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        instance.delete()
        return JsonResponse(status=204)
