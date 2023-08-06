from django.urls import path, re_path, include
from django.contrib.auth import views

from django.contrib.auth.views import LoginView

from .views import HomeView

app_name = "core"

root_urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
]

# Django login accounts views:
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
