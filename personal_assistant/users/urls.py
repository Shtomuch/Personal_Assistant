from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from . import views

from .forms import LoginForm

app_name = "users"

urlpatterns = [
    path("registration/", views.RegisterView.as_view(), name="registration"),
    path(
        "login/",
        views.CustomLoginView.as_view(
            template_name="users/login.html",
            form_class=LoginForm,
            redirect_authenticated_user=True,
            success_url=reverse_lazy("users:profile", kwargs={"username": "username"}),
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("accounts/profile/<str:username>/", views.profile, name="profile"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "reset-password/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url="/users/reset-password/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
