from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('signup/',views.signup),
    path('signin/',views.signin),
    path('logout/',views.logout),
]
