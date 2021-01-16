from pprint import pprint

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import status

from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from event.serializers import *
from event.models import *

from django.db.models import Q


class PlaceView(APIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    
    def get(self):
        data = Place.objects.all()
        serializer = PlaceSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = PlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            pprint(serializer.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            pprint(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        ids = request.GET.get('ids')  # u'2,3,4' <- this is unicode
        if ids is not None:
            ids = ids.split(',')
            data = Profile.objects.filter(pk__in=ids)
            serializer = ProfileSerializer(data, many=True)
            return JsonResponse(serializer.data, safe=False)
    
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class ProfileView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        data = Profile.objects.get(user=request.user.id)
        serializer = ProfileSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = JSONParser().parse(request)
        data["user_id"] = request.user.id
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
    if request.method == "GET":
        data = Follower.objects.filter(follow__id=id_user).only('user_id')
        data = Profile.objects.filter(pk__in=data.values_list('id', flat=True))
        serializer = ProfileSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        try:
            instance = Follower.objects.get(user_id=id_user)
        except Follower.DoesNotExist as e:
            return JsonResponse({"error": "Given Place object not found."}, status=404)
        data = JSONParser().parse(request)
        serializer = FollowerSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = FollowerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        data = Follower.objects.all()
        serializer = FollowerSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def follow(request, id_user):
    if request.method == "GET":
        data = Follower.objects.all().filter(user_id=id_user)
        data = Profile.objects.filter(pk__in=data.values_list('follow__id', flat=True))
        serializer = ProfileSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)


class ActivityView(APIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    
    def get(self, request, *args, **kwargs):
        data = Activity.objects.all()
        serializer = ActivitySerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = ActivitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class EventView(APIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data = Event.objects.all()
        serializer = EventSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = JSONParser().parse(request)
        data["owner_id"] = Profile.objects.get(user=request.user.id).id
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            pprint(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
def participant(request, event_id, state):
    if request.method == "GET":
        data = Participant.objects.filter(Q(event_participant_id_id=event_id) & Q(stat=state)) \
            .only('user_participant_id')
        data = Profile.objects.filter(pk__in=data.values_list('user_participant_id', flat=True))
        serializer = ProfileSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ParticipantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class ParticipantView(APIView):
    
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        event_id = kwargs["event_id"]
        state = kwargs["state"]
        
        data = Participant.objects.filter(Q(event_participant_id_id=event_id) & Q(stat=state)) \
            .only('user_participant_id')
        data = Profile.objects.filter(pk__in=data.values_list('user_participant_id', flat=True))
        serializer = ProfileSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = ParticipantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):
        event_id = kwargs["event_id"]
        user_id = kwargs["state"]
        try:
            instance = Participant.objects.get(Q(event_participant_id_id=event_id) & Q(user_participant_id_id=user_id))
        except Participant.DoesNotExist as e:
            return JsonResponse({"error": "Given Place object not found."}, status=404)
        data = JSONParser().parse(request)
        serializer = ParticipantSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    
    

# @csrf_exempt
# def participant_details(request, ID):
#     try:
#         instance = Participant.objects.get(id=ID)
#     except Participant.DoesNotExist as e:
#         return JsonResponse({"error": "Given Place object not found."}, status=404)
#
#     if request.method == "GET":
#         serializer = ParticipantSerializer(instance)
#         return JsonResponse(serializer.data)
#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = ParticipantSerializer(instance, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=200)
#         return JsonResponse(serializer.errors, status=400)
#     elif request.method == "DELETE":
#         instance.delete()
#         return JsonResponse(status=204)


# @csrf_exempt
# def message(request):
#     if request.method == "GET":
#         data = Message.objects.all()
#         serializer = MessageSerializer(data, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = MessageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def message_details(request, ID):
#     try:
#         instance = Message.objects.get(id=ID)
#     except Message.DoesNotExist as e:
#         return JsonResponse({"error": "Given Place object not found."}, status=404)
#
#     if request.method == "GET":
#         serializer = MessageSerializer(instance)
#         return JsonResponse(serializer.data)
#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = MessageSerializer(instance, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=200)
#         return JsonResponse(serializer.erros, status=400)
#     elif request.method == "DELETE":
#         instance.delete()
#         return JsonResponse(status=204)
