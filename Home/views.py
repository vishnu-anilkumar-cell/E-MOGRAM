from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import *
from .serializer import *
# Create your views here.

@api_view(['POST'])
def UserReg(request):
    if request.method == 'POST':
        data=request.data
        serializer=UserRegSerializer(data=data)
        print(serializer)
        email = data.get('email')

        # Check if a user with the given email already exists
        if Clint.objects.filter(email=email).exists():
            return Response({"output": "0", "message": "Email already exists."}, status=status.HTTP_409_BAD_REQUEST)


        if serializer.is_valid():
            serializer.save()
            return Response({"output": "1"},status=status.HTTP_201_CREATED)
        return Response({"output": "0"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def UserLogin(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        deviceid=request.data.get('deviceid')
        print("device id ===========================================",deviceid)
        if Clint.objects.filter(email=email,password=password,status=1).first() != None:
            #request.session['email']=Clint.objects.filter(email=email,password=password,status=1).first().email
            user=Clint.objects.filter(email=email,password=password,status=1).first()
            Logined.objects.create(user=user,device_token=deviceid)
            return Response({"message": "Login successful","email":Clint.objects.filter(email=email,password=password,status=1).first().email}, status=status.HTTP_200_OK)
        else:
            return Response({ "message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
def DoctorLogin(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        if Doctor.objects.filter(email=email,password=password,status=1).first() != None:
            #request.session['docemail']=Doctor.objects.filter(email=email,password=password,status=1).first().email
            return Response({"message": "Login successful","email":Doctor.objects.filter(email=email,password=password,status=1).first().email}, status=status.HTTP_200_OK)
        else:
            return Response({ "message": "Invalid credentialss"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def DoctorLogin1(request):#already loged in
    if 'docemail' in request.session:
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({ "message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def UserLogin1(request):#already loged in
    if 'email' in request.session:
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({ "message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def DoctorLogout(request):
    if 'docemail' in request.session:
        del request.session['docemail']
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    else:
        return Response({ "message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def UserLogout(request):
    if request.method == 'POST':
        email = request.data.get('email')
        user=Clint.objects.filter(email=email).first()
        ld=Logined.objects.filter(user=user).last()
        ld.delete()
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    if 'email' in request.session:
        del request.session['email']
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    else:
        return Response({ "message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

