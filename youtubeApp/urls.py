from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('signup/',views.signup),
    path('signin/',views.signin),
    path('logout/',views.logout),
    path('upload_video/',views.upload_video),
    re_path('^play_video/(?P<id>\d+)/$',views.play_video),
    path('like/',views.like),
    path('dislike/',views.dislike),
]
