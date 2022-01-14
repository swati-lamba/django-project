from django.urls import path
from . import views
from django.conf import settings

app_name = 'users'
assert isinstance(settings.STATIC_URL, object)
urlpatterns = [
                path('register', views.register, name='register'),
                path('profile/<str:username>', views.profile, name='profile'),
                path('login', views.login_user, name='login'),
                path('logout', views.logout_user, name='logout'),
                path('profile/<str:username>/edit', views.edit_profile, name='editProfile'),
                path('profile/<str:username>/save', views.save, name='save')
              ]
