from django.urls import path
from . import views as user_views

app_name = "users"

urlpatterns = [
    path("login/", user_views.LoginView.as_view(), name="login"),
    path("logout/", user_views.log_out, name="logout"),
    path("signup/", user_views.SignUpView.as_view(), name="signup"),
    path("<int:pk>/", user_views.UserProfileView.as_view(), name="profile"),
    path("update/", user_views.UserUpdateProfile.as_view(), name="update"),
    path("change/", user_views.UserChangePassword.as_view(), name="change-password"),
    path(
        "verify/<str:key>/",
        user_views.complete_verification,
        name="complete_verification",
    ),
    path("login/github/", user_views.github_login, name="github_login"),
    path("login/github/callback/", user_views.github_callback, name="github_callback"),
    path("login/kakao/", user_views.kakao_login, name="kakao_login"),
    path("login/kakao/callback/", user_views.kakao_callback, name="kakao_callback"),
    path("switch-hosting/", user_views.switch_hosting, name="switch_hosting"),
    path("switch-language/", user_views.switch_language, name="switch_language"),
]
