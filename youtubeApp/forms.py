
from django import forms
from django.db import models
from youtubeApp.models import User
class signUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    channel_name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    profile = forms.FileField(required=False,widget = forms.FileInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control','required':False}))
    class Meta:
        model = User
        fields = '__all__'

class signInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control','required':False}))

