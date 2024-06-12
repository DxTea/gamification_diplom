from django.urls import path
from django.contrib.auth import views as auth_views

from users import views as user_views

app_name = 'users'
urlpatterns = [
    path('login/', user_views.CustomLoginView.as_view(), name='login'),
    path("register/", user_views.RegisterView.as_view(), name='register'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('<str:username>/', user_views.UserProfileView.as_view(), name='user_profile'),
]
