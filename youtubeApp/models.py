from django.db import models

# Create your models here.

def get_profile_path(instance,filename):
    return "images/profiles/"+instance.username+".jpg"

class User(models.Model):
    username = models.CharField(primary_key=True,max_length=20)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    channel_name = models.CharField(max_length=30)
    profile = models.FileField(upload_to=get_profile_path,null=True)
    password = models.CharField(max_length=100)