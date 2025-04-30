from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
from rest_framework import status
from Home.models import *
from .serializer import *



@api_view(['GET','PUT'])
def UserProfile(request):
    if request.method == 'GET':
        email=request.data.get('email')
        clnt=Clint.objects.filter(email=email).first()
        serializer=UserProfileSerializer1(clnt)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        email=request.data.get('email')
        clnt=Clint.objects.filter(email=email).first()
        data=request.data
        serializer=UserProfileSerializer(clnt,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            clnt=Clint.objects.filter(email=email).first()
            clnt.ProfileUpdated=1
            clnt.save()
            return Response({"output": "1"},status=status.HTTP_201_CREATED)
        return Response({"output": "0"},status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def UserHome(request):
    if request.method == 'GET':
        email=request.data.get('email')
        clnt=Clint.objects.filter(email=email).first()
        if clnt.ProfileUpdated==1:
            return Response({"name":clnt.name},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def PreviousChats(request):
    email=request.data.get('email')
    r=Room.objects.filter(User=email)
    r=RoomSerializer(r,many=True)
    return Response({"chats":r.data}) 

@api_view(['GET'])
def ViewDoctors(request):
    doctors=Doctor.objects.all()
    doctors=DoctorsSerializer(doctors,many=True)
    return Response({"doctors":doctors.data}) 


@api_view(['GET'])
def ViewDoctorsMore(request):
    id=request.data.get("email")
    print(id)
    doctor=Doctor.objects.filter(email=id).first()
    print(doctor)
    doctor=DoctorsSerializer(doctor)
    return Response({"doctors":doctor.data}) 


@api_view(['GET'])
def ViewMessages(request):
    id=request.data.get('roomid')
    r=Room.objects.filter(id=id).first()
    chats=Chat.objects.filter(Room=r)
    c=ChatSerilizer(chats,many=True)
    return Response({"chats":c.data})

@api_view(['POST'])
def SendMessage(request):
    id=request.data.get('roomid')
    msg=request.data.get('message')
    r=Room.objects.filter(id=id).first()
    chats=Chat.objects.create(Room=r,msg=msg,SendFrom=1)
    return Response({"output": "1"},status=status.HTTP_201_CREATED)

@api_view(['POST'])
def BookAppoinment(request):
    user=request.data.get('user_email')
    doctor=request.data.get('doc_email')
    bookdate=request.data.get('date')
    timesloat=request.data.get('timeloat')
    doctor=Doctor.objects.filter(email=doctor).first()
    user=Clint.objects.filter(email=user).first()


    ## CHCK ALREADY BOOKED OR NOT . IF NOT THEN BOOK THAT SLOT

    if BookDoctor.objects.filter(doctor=doctor,bookdate=bookdate,timesloat=timesloat).first()  == None:
        BookDoctor.objects.create(doctor=doctor,User=user,bookdate=bookdate,timesloat=timesloat)
        return Response({"output": "1"},status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

from datetime import date,timedelta

@api_view(['GET'])
def ViewMyBookings(request):
    id=request.data.get("email") 
    user=Clint.objects.filter(email=id).first()
    today = date.today()
    bk = BookDoctor.objects.filter(User=user, bookdate__gte=today,Room__isnull=True).order_by('-bookdate')
    bk=BookSerilizer(bk,many=True)
    return Response({"BOOKINGS":bk.data},status=status.HTTP_200_OK)

@api_view(['GET'])
def StartChat(request):
    id=request.data.get("bookid")
    book=BookDoctor.objects.filter(id=id).first()

    if book.Room is None:

        id=Room.objects.create(doctor=book.doctor,User=book.User)
        book.Room=id
        book.save()
        print("NOt have a room creating new one ")
    
    return Response({"Room":book.Room.id,"Doctor_Name":book.doctor.name},status=status.HTTP_200_OK)


    
    


    

     





