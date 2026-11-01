from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class EmailVerifiedMixin(AccessMixin):
    """Разрешает доступ только пользователям с email_verified = True"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.email_verified:
            raise PermissionDenied(
                "Для доступа необходимо подтвердить email."
            )

        return super().dispatch(request, *args, **kwargs)