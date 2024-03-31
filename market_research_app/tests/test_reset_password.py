from utility.constants import BASE_URL
from utility.constants import *
from ..models import User
from django.utils.timezone import timedelta
from utility.test_utility import *
from datetime import datetime

"""Model"""
from ..models import User

class ResetPasswordTest(BaseTestCase):
    model_class = User

    @classmethod
    def setUpTestData(self):
        self.user ,created = self.model_class.objects.get_or_create(
            first_name = "demo",
            last_name = "user",
            email = "demo11@test.com",
            mobile = 9988776655,
            username = "userdemo",
            role_id = SUPER_ADMIN_ROLE,
            email_hash = "abcd",
            hash_time = timezone.now()
            )
        self.user.set_password("reset123")
        self.user.save()
        self.auth_headers = get_auth_dict(self.user)
        
        self.user2 ,created = self.model_class.objects.get_or_create(
            first_name = "user",
            last_name = "demo",
            email = "demo@test.com",
            mobile = 9988336655,
            username = "demo",
            role_id = SUPER_ADMIN_ROLE,
            email_hash = "dscbd",
            hash_time = timezone.now()-timedelta(1),
            )
        self.user.set_password("reset123")
        self.user.save()
        
        self.inactive_user, created = self.model_class.objects.get_or_create(
            first_name = "demo1",
            last_name = "user2",
            email = "demo22@test.com",
            mobile = 9988771155,
            username = "demouser",
            role_id = SUPER_ADMIN_ROLE,
            email_hash = "okdsfj",
            hash_time = timezone.now(),
            status = STATUS_INACTIVE
            )
        self.inactive_user.set_password("reset123")
        self.inactive_user.save()

    url = BASE_URL + "reset-password/"
    data = dict()

    # test reset passward api valid unit test
    def test_reset_password_api_valid(self):
        url = self.url + str("?token=") + self.user.email_hash
        self.data["email"] = self.user.email
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "reset123"
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 200)

    # test reset passward api invalid unit test
    def test_reset_password_api_invalid_password_and_confirm_password(self):
        url = self.url + str("?token=") + self.user.email_hash
        self.data["email"] = self.user.email
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "123"
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 400)

    # test reset passward api invalid unit test
    def test_reset_password_api_invalid_link_expires(self):
        url = self.url + str("?token=") + self.user2.email_hash
        self.data["email"] = self.user2.email
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "reset123"
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 400)

    # test reset passward api invalid unit test
    def test_change_password_api_wrong_password(self):
        self.data["email"] = self.user.email
        self.data["password"] = ""
        self.data["confirm_password"] = "reset123"
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)

        # test reset passward api invalid unit test
    def test_change_password_api_invalid_token_required(self):
        self.data["email"] = self.user.email
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "reset123"
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)

        # test reset passward api invalid unit test
    def test_change_password_api_invalid_email_or_token(self):
        url = self.url + str("?token=") + self.user2.email_hash
        self.data["email"] = self.user.email
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "reset123"
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 404)
        
    # test reset passward api invalid unit test
    def test_reset_password_api_invalid_user_not_active(self):
        url = self.url + str("?token=") + self.inactive_user.email_hash
        self.data["email"] = self.inactive_user.email
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "reset123"
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 400)