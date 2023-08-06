from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from ..helpers import has_mfa


class NoopTokenSerializer(serializers.Serializer):
    """dj-rest-auth requires tokens, but we don't use them."""


class MFALoginSerializer(LoginSerializer):
    def authenticate(self, **kwargs):
        user = authenticate(self.context["request"], **kwargs)
        if user:
            has_mfa(self.request, user)

        return user
