from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from .forms import ProfileEditForm
from .models import AdvUser


def index(request):
    return render(request, "main/index.html")


def other_page(request, page):
    try:
        template = get_template("main/" + page + ".html")
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class BBLoginView(LoginView):
    template_name = "main/login.html"


class BBLogoutView(LogoutView):
    pass


@login_required
def profile(request):
    return render(request, "main/profile.html")


class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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
