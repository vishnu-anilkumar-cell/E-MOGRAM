from . import views
from django.urls import path

app_name="Admin"

urlpatterns = [
    path('', views.login, name='login'),
    path('home', views.home, name='home'),
    path('adddoctor', views.adddoctor, name='adddoctor'),
    path('update_doctor/<str:email>', views.update_doctor, name='update_doctor'),
    path('viewdoctors', views.viewdoctors, name='viewdoctors'),
    path('delete_doctor/<str:email>', views.delete_doctor, name='delete_doctor'),
    path('viewusers', views.viewusers, name='viewusers'),
    path('viewappoiments', views.viewappoiments, name='viewappoiments'),
    path('FetchPosts', views.FetchPosts, name='FetchPosts'),
    path('SendNotification', views.SendNotification, name='SendNotification'),

]