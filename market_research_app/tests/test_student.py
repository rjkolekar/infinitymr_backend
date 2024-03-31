
# from utility.test_utility import BaseTestCase
# from utility.constants import BASE_URL
# from oauth2_provider.models import AccessToken
# from utility.constants import *
# from django.utils import timezone
# import requests
# from json import loads, dumps
# from utility.test_utility import *
# from oauthlib.common import generate_token
# from stark_utilities.utilities import random_string_generator
# from django.conf import settings
# from datetime import date, datetime

# ##Model
# from ..models import Student, User, Roles


# class StudentTest(BaseTestCase):
#     model_class =  Student

#     @classmethod
#     def setUpTestData(self):
#         self.user = create_user(SUPERUSER_ROLE)
#         self.admin_user, created = User.objects.get_or_create(first_name="akshay", last_name="gaudse", mobile="8956230023", email='s.superadmin@gmail.com'
#                                         )
#         self.student_instance, created = self.model_class.objects.get_or_create(
#             name=random_string_generator(),
#             email=random_email_generator(),
#             marks = 88,
#             gender = 1,
#             city = "Pune"
#         )
#         self.admin_user.set_password("123456")
#         self.admin_user.save()

#         self.auth_headers = get_auth_dict(self.user)


#     url = BASE_URL + 'student/'
#     data = dict()

#     # Create add valid test
#     def test_add_api_valid(self):
#         print(self.user.role.name,"===")
#         self.data = dict()
#         self.data["name"] = random_string_generator()
#         self.data["city"] = "Pune"
#         self.data["email"] = random_email_generator()
#         self.data['status'] = STATUS_ACTIVE
#         self.data['gender'] = 1
#         response = self.client.post(self.url, data=self.data, **self.auth_headers)
#         self.assertEqual(response.status_code, 201)

#     # Create add invalid test
#     def test_add_api_empty(self):
#         self.data = dict()
#         response = self.client.post(self.url, data=self.data, **self.auth_headers)
#         self.assertEqual(response.status_code, 400)

#     # Update api valid test
#     def test_put_for_api_valid(self):
#         self.url = self.url + str(self.student_instance.id) + '/'
#         self.data['id'] = self.student_instance.id
#         self.data["marks"] = 88
#         response = self.client.put(self.url, data=self.data, **self.auth_headers)
#         self.assertEqual(response.status_code, 200)

#     # Update api invalid test
#     def test_put_for_api_invalid(self):
#         self.url = self.url + str(self.student_instance.id) + '5000000/'
#         self.data['status'] = 1
#         self.data['gender'] = 1
#         response = self.client.put(self.url, data=self.data, **self.auth_headers)
#         self.assertEqual(response.status_code, 404)

#     # List api test
#     def test_get_api_valid(self):
#         response = self.client.get(self.url, **self.auth_headers)
#         self.assertEqual(response.status_code, 200)

#     #Retrieve api test 
#     def test_retrieve_api_valid(self):
#         self.url = self.url + str(self.student_instance.id) + '/'
#         response = self.client.get(self.url, **self.auth_headers)
#         self.assertEqual(response.status_code, 200)

#     #Retrieve invalid id test
#     def test_retrieve_api_invalid(self):
#         self.url = self.url + str(self.student_instance.id) + '5000000/'
#         response = self.client.get(self.url, **self.auth_headers)
#         self.assertEqual(response.status_code, 404)

#     # delete api valid id test
#     def test_del_api_valid(self):
#         self.url = self.url + str(self.student_instance.id) + '/'
#         response = self.client.delete(self.url, **self.auth_headers)
#         self.assertEqual(response.status_code, 200)

#     # delete api invalid id test
#     def test_del_api_invalid(self):
#         self.url = self.url + str(self.student_instance.id) + '5000000/'
#         response = self.client.delete(self.url,**self.auth_headers)
#         self.assertEqual(response.status_code, 404)
        