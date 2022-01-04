from django.shortcuts import redirect, render
from youtubeApp.forms import SignUpForm,SignInForm, VideoUploadForm
from youtubeApp.models import User, Video
from django.contrib.auth.hashers import make_password,check_password
from django.views.decorators.cache import cache_control

# Create your views here.

# def authenticate(func):
#     def inner(request):
#         pass
#     return inner

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_page(request):
    username = request.session.get('username',None)
    if(username):
        user = User.objects.get(username=username)
    else:
        user = None
    videos = Video.objects.all()
    return render(request,'home.html',{"user":user,"videos":videos})

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

def upload_video(request):
    if(request.method == "POST"):
        # file_name = request.FILES["file"]
        # form = VideoUploadForm(request.POST,request.FILES)
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

def play_video(request,id):
    print(id)
    return render(request,"play_video.html")
