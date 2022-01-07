from django.db import models
from django.db.models import constraints
from . import validators
from django.contrib.postgres.fields import ArrayField

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

    def __str__(self):
        return self.username

def video_upload_path(instance,filename):
    return "videos/{}/{}".format(instance.user.username,filename)

class Video(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='videos')
    name = models.CharField(max_length=60)
    description = models.TextField()
    file = models.FileField(upload_to=video_upload_path,validators=[validators.validate_file_extension])
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + "by" + self.user.username

class Like(models.Model):
    video = models.ForeignKey(Video,on_delete=models.CASCADE,related_name="likes")
    by_whom = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="liked_videos")
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['video', 'by_whom'], name='unique_likes_per_video_per_user')
        ]

class DisLike(models.Model):
    video = models.ForeignKey(Video,on_delete=models.CASCADE,related_name="dislikes")
    by_whom = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="disliked_videos")
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['video', 'by_whom'], name='unique_dislikes_per_video_per_user')
        ]

class PlayList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="playlists")
    name = models.CharField(max_length=60)
    modified_date = models.DateTimeField(auto_now=True)
    video_ids = ArrayField(models.IntegerField(),default=list,blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','name'], name="unique_playlist_per_user")
        ]
