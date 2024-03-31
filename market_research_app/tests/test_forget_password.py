import unittest
from utility.constants import BASE_URL
from utility.constants import *
from utility.utils import send_common_email
from ..models import User
from utility.test_utility import *
"""Model"""
from ..models import User

class ForgetPasswordTest(BaseTestCase):
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
        self.auth_headers = get_auth_dict(self.user)
        self.user.set_password("reset123")
        self.user.save()
        
    url = BASE_URL + "forget-password/"
    data = dict()

    # test forget passward api valid unit test
    def test_add_api_valid(self):
        self.data["email"] = self.user.email
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)
        
    # test forget passward api valid unit test
    def test_add_api_valid_is_local(self):
        self.data["is_local"] = True
        self.data["email"] = self.user.email
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)

    # test forget passward api invalid unit test
    def test_add_api_invalid_email(self):
        self.data["email"] = "demo@mail.com"
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 404)
        
    # test forget passward api invalid unit test
    def test_add_api_email_empty(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
        
    # test forget passward api invalid unit test
    def test_forget_password_api_invalid_internal_server_error(self):
        self.data["email"] = self.user.email
        response = self.client.post(self.url, data=[self.data],**self.auth_headers)
        self.assertEqual(response.status_code, 500)
        