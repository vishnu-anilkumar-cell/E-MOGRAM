from django import forms
from Home.models import *

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['email', 'password', 'name', 'age', 'patents', 'experence', 'specialization', 'education', 'about']



class DoctorForm2(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['password', 'name', 'age', 'patents', 'experence', 'specialization', 'education', 'about','status']
