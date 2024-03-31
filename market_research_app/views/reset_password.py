from django.utils import timezone
from rest_framework.generics import CreateAPIView

from utility.constants import FORGET_PASSWORD_TOKEN_EXPIRY_IN_SEC, STATUS_ACTIVE
from ..model.users import User
from ..serializers.reset_password_serializer import ResetPasswordSerializer
from utility.response import ApiResponse
from market_research_app.swagger.reset_password_swagger import swagger_auto_schema

class ResetPasswordView(CreateAPIView, ApiResponse):
    queryset = User.objects.filter(status=STATUS_ACTIVE)
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema
    def post(self, request, *args, **kwargs):
        """
        API for reset password.
        """
        
        data = request.data.copy()
        email = data.get("email")
        token = request.query_params.get("token")
        
        if not email or not token:
            return ApiResponse.response_bad_request(self, message="Email and token is required. ")
        if data.get("password") != data.get("confirm_password"):
            return ApiResponse.response_bad_request(
                self, message="Password and confirm password not match"
            )
        try:
            user = User.objects.get(email=email, email_hash=token)
        except:
            return ApiResponse.response_not_found(self, message="Invalid email or token")
        
        if user.status != STATUS_ACTIVE:
            return ApiResponse.response_bad_request(
                self, message="Please contact admin to activate the account."
            )
        """ Check Expiry Date """
        time_to_expire = (timezone.now() - user.hash_time).total_seconds()
        if time_to_expire >= FORGET_PASSWORD_TOKEN_EXPIRY_IN_SEC:
            user.email_hash = None
            user.hash_time = None
            user.save()
            return ApiResponse.response_bad_request(self, message="Link expires")
        
        user.set_password(data.get("password"))
        user.email_hash = None
        user.hash_time = None
        user.save()
        return ApiResponse.response_ok(self, message="Password changed successfully.")
        
