from django.utils.translation import gettext_lazy as _
from .models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class StatusAwareTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Blocks JWT issuance unless the account is approved (status=Active)."""

    @classmethod
    def get_token(cls, user: User):
        # If user exists but is not approved, refuse token issuance.
        if getattr(user, "status", None) != "Active":
            raise cls.error_class(
                {"detail": _(f"Account not approved (status={user.status}).")}
            )
        return super().get_token(user)

