from .test_setup import TestSetUp
from django.contrib.auth.models import User

class TestViews(TestSetUp):
    
    def test_user_cannot_register_without_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)
    
    def test_user_can_register(self):
        res = self.client.post(self.register_url, self.user_data, format="json")
        # import pdb 
        # pdb.set_trace()
        self.assertEqual(res.data["email"], self.user_data["email"])
        self.assertEqual(res.status_code, 201)
    
    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 403)
    
    def test_user_can_login_after_verification(self):
        res = self.client.post(self.register_url, self.user_data, format="json")
        user = User.objects.get(email=res.data["email"])
        user.is_active = True 
        user.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)