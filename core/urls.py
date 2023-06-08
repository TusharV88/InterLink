from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.acc_settings, name='settings'),
    path('upload/', views.upload, name='upload'),
    path('like-post/', views.like_post, name='like-post'),
    path('profile/<str:pk>/', views.profile_page, name='profile_page'),
    path('follow/', views.follow, name='follow'),
    path('search/', views.search, name='search'),
    path('delete-post/<uuid:post_id>/', views.delete_post, name='delete-post'),
]