from ..model.users import User
from rest_framework.generics import CreateAPIView
from django.conf import settings
from random import randint
from django.template.loader import render_to_string
from utility.utils import encrypt, send_common_email
from random import randint
import urllib.request
from django.utils import timezone
from utility.constants import *

from random import randint
from rest_framework.generics import CreateAPIView
from django.conf import settings
from utility.response import ApiResponse
from random import randint

"""serializer"""
from ..serializers.forget_password_serializer import (
    ForgetPasswordSerializer,
)

"""swagger"""
from ..swagger.forget_password_swagger import swagger_auto_schema

class ForgotPasswordView(CreateAPIView, ApiResponse):
    """
    API Used For validating email and generating Link.
    """

    queryset = User.objects.all().values("email")
    serializer_class = ForgetPasswordSerializer

    def create_email_body(self, user, link):
        context = {"link": link, "logo_url": settings.FRONT_END_URL + "images/login-logo.png"}
        message = render_to_string("forget_password.html", context)
        return message
    
    @swagger_auto_schema
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            email = data.get("email")
            """ Check Eamil NUll"""
            if not email:
                return ApiResponse.response_bad_request(self, message=MESSAGES["email_not_provided"])

            user_instance = User.objects.filter(email=email, status=STATUS_ACTIVE).first()

            if user_instance:
                """ Create hash"""
                random_str = str(randint(100000, 999999))
                email = user_instance.email + random_str
                encrypt_email = encrypt(email).decode("ascii")

                """Save hash in model"""
                user_instance.email_hash = encrypt_email
                user_instance.hash_time = timezone.now()
                user_instance.save()

                # email body
                subject = MESSAGES["forget_password_email_subject"]

                """Create Link"""   
                link = settings.FRONT_END_URL + "reset-password?token=" + urllib.parse.quote_plus(encrypt_email)

                if data.get("is_local"):
                    link = settings.BASE_URL + "password/reset/" + urllib.parse.quote_plus(encrypt_email)

                message = self.create_email_body(user_instance, link)
                email_to = user_instance.email
                from_emails = settings.FROM_EMAIL
                
                # send email
                send_common_email(subject, message, email_to, from_emails)

                return ApiResponse.response_ok(self, message="Link successfully sent to your email.")
            else:
                return ApiResponse.response_not_found(self, message="User with this email does not exist.")
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
