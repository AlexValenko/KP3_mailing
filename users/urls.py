from django.contrib.auth.views import (
    LoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.forms import CustomAuthenticationForm, CustomSetPasswordForm
from users.views import (
    ResendVerificationView,
    UserBlockView,
    UserDetailView,
    UserListView,
    UserLogoutView,
    UserProfileUpdatePassView,
    UserProfileUpdateView,
    UserRegisterView,
    UserStatisticListView,
    UserUnblockView,
    email_verification,
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
    path("email_confirm/<str:token>/", email_verification, name="email_confirm"),
    path("resend_verification/", ResendVerificationView.as_view(), name="resend_verification"),
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="password_reset_form.html",
            email_template_name="password_reset_email.txt",
            subject_template_name="password_reset_subject.txt",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            form_class=CustomSetPasswordForm,
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
