from utility.constants import BASE_URL
from utility.constants import *
from ..models import User
from django.utils.timezone import timedelta
from utility.test_utility import *
from datetime import datetime

"""Model"""
from ..models import User

class ChangePasswordTest(BaseTestCase):
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
            )
        self.user.set_password("123456")
        self.user.save()
        self.auth_headers = get_auth_dict(self.user)

    url = BASE_URL + "change-password/"
    data = dict()

    # test change passward api valid unit test
    def test_change_password_api_valid(self):
        self.data["old_password"] = "123456"
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "reset123"
        response = self.client.post(self.url, data=self.data,**self.auth_headers)
        self.assertEqual(response.status_code, 200)

    # test change passward api invalid unit test
    def test_change_password_api_invalid_password_and_confirm_password(self):
        self.data["old_password"] = "123456"
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "reset3"
        response = self.client.post(self.url, data=self.data,**self.auth_headers)
        self.assertEqual(response.status_code, 400)

    # test change passward api invalid unit test
    def test_change_password_api_empty_invalid(self):
        self.data["old_password"] = ""
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "reset123"
        response = self.client.post(self.url, data=self.data,**self.auth_headers)
        self.assertEqual(response.status_code, 400)

    # test change passward api invalid unit test
    def test_change_password_api_wrong_password(self):
        self.data["old_password"] = "password"
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "reset123"
        response = self.client.post(self.url, data=self.data,**self.auth_headers)
        self.assertEqual(response.status_code, 400)

# test change passward api invalid unit test
    def test_change_password_api_invalid_internal_server_error(self):
        self.data["old_password"] = "123456"
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "reset123"
        response = self.client.post(self.url, data=[self.data],**self.auth_headers)
        self.assertEqual(response.status_code, 500)
   