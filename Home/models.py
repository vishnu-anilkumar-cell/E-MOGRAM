from django.db import models

# Create your models here.
class Clint(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField( max_length=128)
    name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField( blank=True, null=True)
    gender = models.CharField( max_length=10, blank=True, null=True)
    api_key = models.CharField( max_length=500, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    ProfileUpdated=models.IntegerField(default=0)
    status=models.IntegerField(default=1)

class Doctor(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField( max_length=128)
    name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField( blank=True, null=True)
    patents = models.PositiveIntegerField( blank=True, null=True,default=100)
    experence = models.CharField( max_length=128,blank=True, null=True)
    rating = models.IntegerField(default=1)
    specialization = models.CharField( max_length=255, blank=True, null=True)
    education = models.CharField( max_length=255, blank=True, null=True)
    about = models.CharField(blank=True, null=True,max_length=255)
    ProfileUpdated=models.IntegerField(default=0)
    status=models.IntegerField(default=1)


class Admin(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField( max_length=128)
    name = models.CharField(max_length=255, blank=True, null=True)




class Room(models.Model):
    id=models.AutoField(primary_key=True)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    User=models.ForeignKey(Clint,on_delete=models.CASCADE)


class Chat(models.Model):
    Room=models.ForeignKey(Room,on_delete=models.CASCADE)
    msg=models.CharField(max_length=200)
    SendFrom=models.IntegerField() # 1--> Buyer to seller , 2-> sellrt to buyer
    ViewStatus=models.IntegerField(default=0)
    datetime=models.DateTimeField(auto_now=True)


class BookDoctor(models.Model):
    User=models.ForeignKey(Clint,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now=True)  ## BOOKING DONE AT
    bookdate=models.DateField()   ## BOOK TO
    timesloat=models.IntegerField()
    Room=models.ForeignKey(Room,on_delete=models.CASCADE,null=True,blank=True)
    rate=models.FloatField(null=True,blank=True)
    status=models.IntegerField(default=1)




class Logined(models.Model):
    user = models.ForeignKey(Clint, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.device_token}"


