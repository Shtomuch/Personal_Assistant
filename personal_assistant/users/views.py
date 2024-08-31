import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.management import call_command
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib import messages
from django.shortcuts import render

from .forms import RegisterForm, UserProfileForm
from .models import CustomUser


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


class CustomLoginView(LoginView):
    def get_success_url(self):
        username = self.request.user.username
        return reverse("users:profile", kwargs={"username": username})

    def form_invalid(self, form):
        messages.error(self.request, "Wrong username or password")
        return super().form_invalid(form)


@login_required
def profile(request, username):
    call_command("scrape_news")
    try:
        with open("utils/categorized_news.json", "r", encoding="utf-8") as file:
            categorized_news = json.load(file)
    except FileNotFoundError:
        categorized_news = {}

    user = get_object_or_404(CustomUser, username=username)
    if request.method == "POST":
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect("users:profile", username=user.username)

    profile_form = UserProfileForm(instance=request.user)
    return render(
        request,
        "users/profile.html",
        {
            "profile_form": profile_form,
            "user": user,
            "categorized_news": categorized_news,
        },
    )


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "users/password_reset_subject.txt"
