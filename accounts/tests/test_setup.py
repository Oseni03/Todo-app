from rest_framework.test import APITestCase 
from django.urls import reverse
# from faker import Faker  

class TestSetUp(APITestCase):
    
    def setUp(self):
        self.register_url = reverse("accounts:register")
        self.login_url = reverse("accounts:login")
        # faker = Faker()
        
        self.user_data = {
            "username": "username",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email@gmail.com",
            "password": "password1234"
        }
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()