from market_research_app.serializers.change_password_serializer import ChangePasswordSerializer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from utility.utils import *
from rest_framework.permissions import IsAuthenticated
from utility.response import ApiResponse

from market_research.permissions import is_access

"""swagger"""
from ..swagger.change_password_swagger import swagger_auto_schema

class ChangePasswordView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = ChangePasswordSerializer
    authentication_classes = [
        OAuth2Authentication,
    ]
    permission_classes = [IsAuthenticated, is_access]

    @swagger_auto_schema
    def change_password(self, request, *args, **kwargs):
        try:
            """capture data"""
            data = request.data
            user = self.request.user

            if not data.get("old_password") or not data.get("password") or not data.get("confirm_password"):
                return ApiResponse.response_bad_request(self, message="Fields cannot be null")

            """ process/format on data """
            if user.check_password(data.get("old_password")):
                if data.get("password") != data.get("confirm_password"):
                    return ApiResponse.response_bad_request(
                        self, message="Password and confirm password does not match"
                    )
                user.set_password(data.get("password"))
                user.save()
                """ return success """
                return ApiResponse.response_ok(self, message="Password changed successfully")
            else:
                return ApiResponse.response_bad_request(self, "Invalid old password")

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
