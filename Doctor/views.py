from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
from rest_framework import status
from Home.models import *
from .serializer import *

from datetime import date,timedelta


@api_view(['GET','PUT'])
def DoctorProfile(request):
    if request.method == 'GET':
        email=request.data.get('email')
        clnt=Doctor.objects.filter(email=email).first()
        serializer=DoctorProfileSerializer1(clnt)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        email=request.data.get('email')
        clnt=Doctor.objects.filter(email=email).first()
        data=request.data
        serializer=DoctorProfileSerializer(clnt,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            clnt=Doctor.objects.filter(email=email).first()
            clnt.ProfileUpdated=1
            clnt.save()
            return Response({"output": "1"},status=status.HTTP_201_CREATED)
        return Response({"output": "0"},status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def DoctorHome(request):
    if request.method == 'GET':
        email=request.data.get('email')
        clnt=Doctor.objects.filter(email=email).first()
        if clnt.ProfileUpdated==1:
            return Response({"name":clnt.name},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def PreviousChatsDoctor(request):
    email=request.data.get('email')
    r=Room.objects.filter(doctor=email)
    r=RoomSerializer(r,many=True)
    return Response({"chats":r.data}) 




@api_view(['GET'])
def ViewClintMessages(request):
    id=request.data.get('roomid')
    r=Room.objects.filter(id=id).first()
    chats=Chat.objects.filter(Room=r)
    c=ChatSerilizer(chats,many=True)
    return Response({"chats":c.data})

@api_view(['POST'])
def SendClintMessage(request):
    id=request.data.get('roomid')
    msg=request.data.get('message')
    r=Room.objects.filter(id=id).first()
    chats=Chat.objects.create(Room=r,msg=msg,SendFrom=2)
    return Response({"output": "1"},status=status.HTTP_201_CREATED)



@api_view(['GET'])
def StartChatWithClint(request):
    id=request.data.get("bookid")
    book=BookDoctor.objects.filter(id=id).first()
    if book.Room is None:

        id=Room.objects.create(doctor=book.doctor,User=book.User)
        book.Room=id
        book.save()
        print("NOt have a room creating new one ")

    return Response({"Room":book.Room.id,"Clint_name":book.User.name},status=status.HTTP_200_OK)

@api_view(['GET'])
def ViewMyAppoinments(request):
    id=request.data.get("email") 
    user=Doctor.objects.filter(email=id).first()
    today = date.today()
    bk = BookDoctor.objects.filter(doctor=user, bookdate__gte=today).order_by('-bookdate')
    bk=BookSerilizer(bk,many=True)
    return Response({"BOOKINGS":bk.data},status=status.HTTP_200_OK)
