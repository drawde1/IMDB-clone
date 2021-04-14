from django.shortcuts import redirect, render, reverse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from authentication.forms import SignupForm, LoginForm
from IMDB_user.models import MyCustomUser
# Create your views here.


class SignupView(View):
    template_name = "general_form.html"
    form = SignupForm

    def get(self, request):
        form = self.form()
        message = "Sign Up:"
        message_2 = "already have an account?  Go to Login!"
        link = "/login/"
        return render(request, self.template_name, {
            "form": form,
            "message": message,
            "message_2": message_2,
            "link": link
        })

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = MyCustomUser.objects.create_user(
                username=data.get("username"), password=data.get("password"), displayname=data.get("displayname")
            )
            login(request, user)
            return redirect(reverse("homepage"))


class LoginView(View):
    template_name = "login.html"
    form = LoginForm

    def get(self, request):
        form = self.form()
        message = "Log In:"
        message_2 = "don't have an account?  Go to Sign Up!"
        link = "/signup/"
        return render(request, self.template_name, {
            "form": form,
            "message": message,
            "message_2": message_2,
            "link": link
        })

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data.get("username"), password=data.get("password")
            )
            if user:
                login(request, user)
                return redirect(request.GET.get("next", "/"))


def logout_view(request):
    logout(request)
    return redirect(reverse("homepage"))
