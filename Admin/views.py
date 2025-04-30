from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse, response
from django.views.decorators.csrf import csrf_exempt
from .forms import DoctorForm,DoctorForm2
from Home.models import *

# Create your views here.

@csrf_exempt
def login(request):
    if request.method == 'POST':
        print("------ Login Request Processing -------")
        userid=request.POST.get('email')
        password=request.POST.get('password')
        print(request.POST)
        try:
            if userid=="admin@gmail.com" and password=="admin":
                return render(request,'login.html',{"one":1})
            return render(request,'login.html',{"one":2})
        except Exception as e:
            print(e)
            return render(request,'login.html',{"one":2})
    return render(request,'login.html')


@csrf_exempt
def home(request):
    return render(request,'home.html')

@csrf_exempt
def adddoctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_detail')  # Redirect to doctor listing page
    else:
        form = DoctorForm()

    return render(request, 'adddoctor.html', {'form': form})



def viewdoctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'viewdoctors.html', {'doctors': doctors})

def delete_doctor(request, email):
    doctor = get_object_or_404(Doctor, email=email)
    doctor.delete()

    return redirect('Admin:viewdoctors')



def update_doctor(request, email):
    print("UPDATION")
    doctor = get_object_or_404(Doctor, email=email)

    if request.method == 'POST':

        form = DoctorForm2(request.POST, instance=doctor)
        print(form.errors)
        if form.is_valid():
            print("Saved")
            form.save()
            return redirect('Admin:viewdoctors')
        return redirect('Admin:viewdoctors')
    else:
        form = DoctorForm(instance=doctor)  # Populate form with existing doctor data
    return render(request, 'update_doctor.html', {'form': form, 'doctor': doctor})


def viewusers(request):
    users = Clint.objects.all()
    return render(request, 'viewusers.html', {'users': users})

def viewappoiments(request):
    users = BookDoctor.objects.all()
    return render(request, 'viewappoiments.html', {'users': users})

from django.db.models import Q
from fetchpost import fetch_profile_posts
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

def detect_emotion(text):

    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)

    if sentiment_score['compound'] >= 0.05:
        return 'Positive'
    elif sentiment_score['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'





def FetchPosts(request):
    users = Clint.objects.filter(~Q(api_key__isnull=True) & ~Q(api_key=''))
    dict={}
    lis=[]
    for i in users:
        print(i.name)
        posts=fetch_profile_posts(i.api_key)
        for date, details in posts.items():
            dict1={}
            print(f"📅 Date: {date}")
            print(f"🆔 Post ID: {details['Post ID']}")
            print(f"💬 Message: {details['Message']}")
            print(f"😊 Emojis: {details['Emojis']}")
            print("-" * 40)
            dict1["user"]=i.name
            dict1["email"]=i.email
            dict1["date"]=date
            dict1["post"]=details['Message']
            dict1["emotion"] = detect_emotion(details['Message'])

            lis.append(dict1)
    dict["posts"]=lis
    return render(request, 'userposts.html', dict)





from firebase_admin import messaging
from firebase_admin import credentials, messaging, initialize_app

cred = credentials.Certificate("/home/vishnuanil/Emogram/EMORGAM/wellnest1-firebase-adminsdk-5fs9s-440c0baa50.json")
initialize_app(cred)

def send_push_notification(user_id, title, body, data=None):
    """
    Send a push notification to a user's device.
    :param user_id: Unique identifier for the user
    :param title: Notification title
    :param body: Notification body
    :param data: Additional data payload (optional)
    """
    token = user_id
    if not token:
        print(f"No device token found for user {user_id}")
        return

    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=token,
            data=data or {},
        )

        response = messaging.send(message)
        print(f"Notification sent to user {user_id}: {response}")
    except Exception as e:
        print(f"Failed to send notification to user {user_id}: {str(e)}")

def SendNotification(request):
    if request.method == 'POST':
        user = request.POST.get('email')  # Get the email from POST data
        if not user:
            return JsonResponse({"error": "Email is required"}, status=400)

        try:
            cld = Clint.objects.get(email=user)

            token = Logined.objects.filter(user=cld).last()
            if not token or not token.device_token:
                return JsonResponse({"error": "No valid device token found for this user"}, status=404)

            send_push_notification(token.device_token, "Alert", "Book a doctor now, your Facebook posts are sad.")
            return JsonResponse({"success": "Notification sent successfully"})

        except Clint.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
