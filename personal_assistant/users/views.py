from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.shortcuts import render

from .forms import RegisterForm, UserProfileForm


def home(request):
    return render(request, "users/base.html")


class RegisterView(View):
    template_name = "users/registration.html"
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="users:login")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Account created successfully")
            return redirect(to="users:login")
        return render(request, self.template_name, {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect(to="users:profile")

    profile_form = UserProfileForm(instance=request.user)
    return render(request, "users/profile.html", {"profile_form": profile_form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "users/password_reset_subject.txt"
