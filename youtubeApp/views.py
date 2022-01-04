from django.shortcuts import redirect, render
from youtubeApp.forms import signUpForm,signInForm
from youtubeApp.models import User
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
    return render(request,'home.html',{"user":user})

def signup(request):
    if(request.method == "POST"):
        form = signUpForm(request.POST,request.FILES)
        if(form.is_valid()):
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            return redirect('/youtubeApp/signin/')
    else:
        form = signUpForm()
    return render(request,'signup.html',{"form":form})

def signin(request):
    error_message = ""
    if(request.method == "POST"):
        form = signInForm(request.POST)
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
        form = signInForm()
    return render(request,'signin.html',{"form":form,"error_message":error_message})

def logout(request):
    request.session.pop("username",None)
    return redirect("/youtubeApp/")
