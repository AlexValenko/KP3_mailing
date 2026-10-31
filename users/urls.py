from django.contrib.auth.views import LoginView
from django.urls import path

from users.apps import UsersConfig
from users.forms import CustomAuthenticationForm
from users.views import (
    UserLogoutView,
    UserProfileUpdatePassView,
    UserProfileUpdateView,
    UserRegisterView,
    UserStatisticListView,
    UserListView,
    UserDetailView,
UserBlockView,
UserUnblockView,
)

app_name = UsersConfig.name

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="login.html", authentication_form=CustomAuthenticationForm),
        name="login",
    ),
    path("logout/", UserLogoutView.as_view(next_page="mailing:home"), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("profile/edit/<int:pk>/", UserProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/edit_pass/", UserProfileUpdatePassView.as_view(), name="profile_edit_pass"),
    path("profile/statistic/", UserStatisticListView.as_view(), name="statistic"),
    path("users_list/", UserListView.as_view(), name="users_list"),
   path("user/<int:pk>/", UserDetailView.as_view(), name="users_detail"),
    path("user/<int:pk>/block", UserBlockView.as_view(), name="block_user"),
path("user/<int:pk>/unblock", UserUnblockView.as_view(), name="unblock_user"),
]
