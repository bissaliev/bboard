from django.urls import path

from .views import (
    BBLoginView,
    BBLogoutView,
    PasswordEditView,
    ProfileEditView,
    index,
    other_page,
    profile,
)

app_name = "main"

urlpatterns = [
    path("", index, name="index"),
    path("<str:page>/", other_page, name="other"),
    path("accounts/login/", BBLoginView.as_view(), name="login"),
    path("accounts/logout/", BBLogoutView.as_view(), name="logout"),
    path("accounts/profile/", profile, name="profile"),
    path(
        "accounts/profile/edit/",
        ProfileEditView.as_view(),
        name="profile_edit",
    ),
    path(
        "accounts/password/edit/",
        PasswordEditView.as_view(),
        name="password_edit",
    ),
]
