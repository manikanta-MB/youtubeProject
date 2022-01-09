import re
from django.http import request
from django.shortcuts import redirect, render
from youtubeApp.forms import ProfileChangeForm, SignUpForm,SignInForm, VideoUploadForm
from youtubeApp.models import DisLike, Like, PlayList, User, Video
from django.contrib.auth.hashers import make_password,check_password
from django.views.decorators.cache import cache_control
from django.http.response import JsonResponse
from django.core.exceptions import PermissionDenied
import json

# Create your views here.

# def authenticate(func):
#     def inner(request):
#         pass
#     return inner

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_page(request):
    username = request.session.get('username',None)
    if(username):
        user = User.objects.get(username=username)
    else:
        user = None
    videos = Video.objects.all()
    profile_change_form = ProfileChangeForm()
    context = {
        "user":user,
        "videos":videos,
        "profile_change_form":profile_change_form
    }
    return render(request,'home.html',context)

def signup(request):
    if(request.method == "POST"):
        form = SignUpForm(request.POST,request.FILES)
        if(form.is_valid()):
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            return redirect('/youtubeApp/signin/')
    else:
        form = SignUpForm()
    return render(request,'signup.html',{"form":form})

def signin(request):
    error_message = ""
    if(request.method == "POST"):
        form = SignInForm(request.POST)
        given_username = request.POST["username"]
        given_password = request.POST["password"]
        try:
            user = User.objects.get(username=given_username)
            if(check_password(given_password,user.password)):
                request.session["username"] = given_username
                return redirect("/youtubeApp/")
        except:
            pass
        finally:
            error_message = "invalid Username or Password"
    else:
        form = SignInForm()
    return render(request,'signin.html',{"form":form,"error_message":error_message})

def logout(request):
    request.session.pop("username",None)
    return redirect("/youtubeApp/")

def profile_change(request):
    if(request.method == "POST"):
        username = request.POST["username"]
        user = User.objects.get(username = username)
        user.profile = request.FILES["profile"]
        user.save()
        return JsonResponse({"changed":True,"url":user.profile.url})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload_video(request):
    if(request.method == "POST"):
        form = VideoUploadForm(request.POST,request.FILES)
        if(form.is_valid()):
            video = form.save(commit=False)
            current_username = request.session.get("username")
            current_user = User.objects.get(username=current_username)
            video.user = current_user
            video.save()
            return redirect("/youtubeApp/")
    else:
        form = VideoUploadForm()
    return render(request,"upload-video.html",{"form":form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def play_video(request,id):
    remaining_videos = Video.objects.exclude(id=id)
    video_to_watch = Video.objects.get(id=id)
    username = request.session.get('username',None)
    if(username):
        user = User.objects.get(username=username)
    else:
        user = None
    is_like_existed = Like.objects.filter(video=video_to_watch,by_whom=user).exists()
    is_dislike_existed = DisLike.objects.filter(video=video_to_watch,by_whom=user).exists()
    profile_change_form = ProfileChangeForm()
    context = {
        "user":user,
        "remaining_videos":remaining_videos,
        "video_to_watch":video_to_watch,
        "is_like_existed":is_like_existed,
        "is_dislike_existed":is_dislike_existed,
        "profile_change_form":profile_change_form
    }
    return render(request,"play-video.html",context)

def like(request):
    data = json.loads(request.body)
    user = User.objects.get(username = data["username"])
    video = Video.objects.get(id = data["videoId"])
    try:
        DisLike.objects.filter(video=video,by_whom=user).delete()
    except DisLike.DoesNotExist:
        pass
    count = Like.objects.filter(video=video,by_whom=user).delete()[0]
    if(count):
        created = False
    else:
        Like.objects.create(video=video,by_whom=user)
        created = True
    return JsonResponse({"created":created})
def dislike(request):
    data = json.loads(request.body)
    user = User.objects.get(username = data["username"])
    video = Video.objects.get(id = data["videoId"])
    try:
        Like.objects.filter(video=video,by_whom=user).delete()
    except Like.DoesNotExist:
        pass
    count = DisLike.objects.filter(video=video,by_whom=user).delete()[0]
    if(count):
        created = False
    else:
        DisLike.objects.create(video=video,by_whom=user)
        created = True
    return JsonResponse({"created":created})
def get_playlists(request):
    data = json.loads(request.body)
    username = data["username"]
    video_id = int(data["videoId"])
    playlists_objs = PlayList.objects.filter(user__username=username).order_by("-modified_date")
    playlists = []
    for playlist_obj in playlists_objs:
        if(video_id in playlist_obj.video_ids):
            checked=True
        else:
            checked=False
        playlists.append({
            "id":playlist_obj.id,
            "name":playlist_obj.name,
            "checked":checked
        })
    result = {"data":playlists}
    return JsonResponse(result)

def add_to_playlist(request):
    data = json.loads(request.body)
    username = data["username"]
    if(request.session.get("username",None)==username):
        checked = data["checked"]
        video_id = data["videoId"]
        play_list_id = data["playListId"]
        playlist = PlayList.objects.get(id=play_list_id)
        if(checked):
            print("checked")
            playlist.video_ids.append(int(video_id))
        else:
            playlist.video_ids.remove(int(video_id))
        playlist.save()
        return JsonResponse({"success":True})
    else:
        raise PermissionDenied()

def create_new_playlist(request):
    data = json.loads(request.body)
    username = data["username"]
    user = User.objects.get(username=username)
    play_list_name = data["playListName"]
    existed = PlayList.objects.filter(user=user,name=play_list_name).exists()
    if(existed):
        return JsonResponse({"existed":True})
    else:
        playlist = PlayList.objects.create(user=user,name=play_list_name)
        return JsonResponse({"success":True,"playListId":playlist.id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def playlists(request):
    username = request.session.get('username',None)
    if(username):
        user = User.objects.get(username=username)
    else:
        user = None
    playlists = PlayList.objects.filter(user__username=username).order_by("-modified_date")
    profile_change_form = ProfileChangeForm()
    context = {
        "profile_change_form":profile_change_form,
        "playlists":playlists,
        "user":user
    }
    return render(request,'playlists.html',context)

def get_videos_by_playlist(request):
    data = json.loads(request.body)
    playlist_id = data["playListId"]
    playlist_obj = PlayList.objects.get(id=playlist_id)
    if(len(playlist_obj.video_ids)>0):
        video_urls,video_ids,video_user_names,video_names,uploaded_dates = [],[],[],[],[]
        for id in playlist_obj.video_ids:
            video = Video.objects.get(id=id)
            video_urls.append(video.file.url)
            video_ids.append(id)
            video_user_names.append(video.user.username)
            video_names.append(video.name)
            uploaded_dates.append(video.uploaded_date.date())
            result = {
                "urls":video_urls,
                "ids":video_ids,
                "videoNames":video_names,
                "userNames":video_user_names,
                "uploadedDates":uploaded_dates
            }
    else:
        result = {"nothing":True}
    return JsonResponse(result)

def remove_playlist(request):
    data = json.loads(request.body)
    playlist_id = data["playListId"]
    PlayList.objects.filter(id=playlist_id).delete()
    return JsonResponse({"deleted":True})

def remove_video_from_playlist(request):
    data = json.loads(request.body)
    playlist_id = data["playListId"]
    video_id = data["videoId"]
    playlist_obj = PlayList.objects.get(id=playlist_id)
    playlist_obj.video_ids.remove(int(video_id))
    playlist_obj.save()
    return JsonResponse({"deleted":True})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def your_videos(request):
    username = request.session.get('username',None)
    if(username):
        user = User.objects.get(username=username)
    else:
        user = None
    videos = Video.objects.filter(user__username=username)
    profile_change_form = ProfileChangeForm()
    context = {
        "user":user,
        "videos":videos,
        "profile_change_form":profile_change_form
    }
    return render(request,'your_videos.html',context)

def delete_video(request):
    data = json.loads(request.body)
    video_id = data["videoId"]
    Video.objects.filter(id=video_id).delete()
    return JsonResponse({"deleted":True})
