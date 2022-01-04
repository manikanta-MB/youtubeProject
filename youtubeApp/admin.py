from django.contrib import admin
from youtubeApp.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["username","first_name","last_name","channel_name","profile"]

admin.site.register(User,UserAdmin)
