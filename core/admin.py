from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id_user']


class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'caption', 'created_at']



class LikePostAdmin(admin.ModelAdmin):
    list_display = ['username', 'post_id']


class FollowersCountAdmin(admin.ModelAdmin):
    list_display = ['user', 'followers']



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(LikePost, LikePostAdmin)
admin.site.register(FollowersCount, FollowersCountAdmin)