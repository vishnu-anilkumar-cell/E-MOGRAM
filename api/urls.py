from Home import views  
from User import views as v1
from Doctor import views as v2
from django.urls import path
urlpatterns = [

    ## Home

    path('UserReg',views.UserReg,name='UserReg'),
    path('UserLogin',views.UserLogin,name='UserLogin'),
    path('DoctorLogin',views.DoctorLogin,name='DoctorLogin'),
    path('UserLogin1',views.UserLogin1,name='UserLogin1'),
    path('DoctorLogin1',views.DoctorLogin1,name='DoctorLogin1'),

    ## User
    path('UserLogout',views.UserLogout,name='UserLogout'),
    path('UserHome',v1.UserHome,name='UserHome'),
    path('UserProfile',v1.UserProfile,name='UserProfile'),
    path('UserProfile',v1.UserProfile,name='UserProfile'),
    path('PreviousChats',v1.PreviousChats,name='PreviousChats'),
    path('ViewDoctors',v1.ViewDoctors,name='ViewDoctors'),
    path('ViewDoctorsMore',v1.ViewDoctorsMore,name='ViewDoctorsMore'),
    path('ViewMessages',v1.ViewMessages,name='ViewMessages'),
    path('SendMessage',v1.SendMessage,name='SendMessage'),
    path('BookAppoinment',v1.BookAppoinment,name='BookAppoinment'),
    path('ViewMyBookings',v1.ViewMyBookings,name='ViewMyBookings'),
    path('StartChat',v1.StartChat,name='StartChat'),
    



    ##Doctor
    path('DoctorLogout',views.DoctorLogout,name='DoctorLogout'),
    path('DoctorHome',v2.DoctorHome,name='DoctorHome'),
    path('DoctorProfile',v2.DoctorProfile,name='DoctorProfile'),

    path('PreviousChatsDoctor',v2.PreviousChatsDoctor,name='PreviousChatsDoctor'),
    path('ViewClintMessages',v2.ViewClintMessages,name='ViewClintMessages'),
    path('SendClintMessage',v2.SendClintMessage,name='SendClintMessage'),
    path('ViewMyAppoinments',v2.ViewMyAppoinments,name='ViewMyAppoinments'),
    path('StartChatWithClint',v2.StartChatWithClint,name='StartChatWithClint'),





]