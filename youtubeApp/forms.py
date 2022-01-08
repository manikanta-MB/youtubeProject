from django import forms
from youtubeApp.models import User, Video

class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    channel_name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    profile = forms.FileField(required=False,widget = forms.FileInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control','required':False}))
    class Meta:
        model = User
        fields = '__all__'

class SignInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control','required':False}))

class VideoUploadForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    file = forms.FileField(widget = forms.FileInput(attrs={'class':'form-control','accept':'video/*'}))
    class Meta:
        model = Video
        fields = ("name","description","file")

class ProfileChangeForm(forms.Form):
    profile = forms.FileField(widget = forms.FileInput(attrs={'accept':'.jpg,.jpeg,.png'}))
