from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ProfileEditForm, RegisterForm
from .models import AdvUser
from .utilities import signer


def index(request):
    return render(request, "main/index.html")


def other_page(request, page):
    try:
        template = get_template("main/" + page + ".html")
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class BBLoginView(LoginView):
    """Класс-представление для входа пользователя."""

    template_name = "main/login.html"


class BBLogoutView(LogoutView):
    pass


@login_required
def profile(request):
    return render(request, "main/profile.html")


class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Редактирование личных данных пользователя."""

    model = AdvUser
    template_name = "main/profile_edit.html"
    form_class = ProfileEditForm
    success_url = reverse_lazy("main:profile")
    success_message = "Данные пользователя изменены"

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class PasswordEditView(
    SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView
):
    template_name = "main/password_edit.html"
    success_url = reverse_lazy("main:profile")
    success_message = "Пароль пользователя изменен"


class RegisterView(CreateView):
    model = AdvUser
    template_name = "main/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("main:register_done")


class RegisterDoneView(TemplateView):
    template_name = "main/register_done.html"


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, "main/activation_failed.html")
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = "main/activation_done_earlier.html"
    else:
        template = "main/activation_done.html"
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class ProfileDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = "main/profile_delete.html"
    success_url = reverse_lazy("main:index")
    success_message = "Пользователь удален"

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def rubric_bbs(request, pk):
    pass
