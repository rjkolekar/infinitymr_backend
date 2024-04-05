
from utility.constants import BASE_URL
from utility.constants import *
from utility.test_utility import *


##Model
from ..models import Contactdetails


class ContactdetailsTest(BaseTestCase):
    model_class =  Contactdetails

    @classmethod
    def setUpTestData(self):
        self.user = create_user(SUPERUSER_ROLE)
        self.auth_headers = get_auth_dict(self.user)
        self.user.set_password("reset123")
        self.user.save()
        self.get_instance, created = self.model_class.objects.get_or_create(id=1)
        


    url = BASE_URL + 'contactdetails/'
    data = dict()

    #Create add valid test
    def test_add_api_valid(self):
        
        self.data['email'] = str(random_string_generator()) + '@test.com'
        response = self.client.post(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 201)

    # #Create add invalid test
    def test_add_api_empty(self):
        self.data = dict()
        response = self.client.post(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 400)

    # #Update api valid test
    def test_put_for_api_valid(self):
        
        self.data['email'] = str(random_string_generator()) + '@test.com'
        self.data['id'] = self.get_instance.id
        response = self.client.put(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    # #Update api invalid test
    def test_put_for_api_invalid(self):
        
        self.data['email'] = str(random_string_generator()) + '@test.com'
        self.data['id'] = 110000
        response = self.client.put(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 404)

    #List api test
    def test_get_api_valid(self):
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    #Retrieve api test 
    def test_retrieve_api_valid(self):
        url = self.url + str(self.get_instance.id) + '/'
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    #Retrieve invalid id test
    def test_retrieve_api_invalid(self):
        url = self.url + '50000/'
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, 404)

    #delete api valid id test
    def test_del_api_valid(self):
        url = self.url + str(self.get_instance.id) + '/'
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    #delete api invalid id test
    def test_del_api_invalid(self):
        url = self.url + '5000000/'
        response = self.client.delete(url,**self.auth_headers)
        self.assertEqual(response.status_code, 404)
        