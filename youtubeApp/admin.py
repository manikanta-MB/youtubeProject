from django.contrib import admin
from youtubeApp.models import User,Video

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["username","first_name","last_name","channel_name","profile"]

class VideoAdmin(admin.ModelAdmin):
    list_display = ["user","name","description","file","uploaded_date"]

admin.site.register(User,UserAdmin)
admin.site.register(Video,VideoAdmin)
