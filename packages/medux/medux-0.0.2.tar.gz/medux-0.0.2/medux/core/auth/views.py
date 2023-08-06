from django.contrib.auth.views import LoginView as DjangoLoginView
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin

from .forms import LoginForm, SignUpForm


class LoginView(DjangoLoginView):
    template_name = "registration/login.html"
    # form_class = LoginForm
    message = ""
    extra_context = {"message": message}

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class(initial=self.extra_context)
    #     return render(
    #         request,
    #         self.template_name,
    #         {"form": form, "message": self.message},
    #     )


#
#     def post(self, request: HttpRequest, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             if user is not None:
#                 login(request, user)
#                 return redirect("")
#             else:
#                 self.message = _("Nope")
#         else:
#             self.message = _("Error validating toe login form")


def register_user(request):

    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = "User created"
            success = True

            # return redirect("/login/")

        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(
        request,
        "accounts/user-add.html",
        {"form": form, "msg": msg, "success": success},
    )
