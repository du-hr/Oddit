from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import CustomUser
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class createUserApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        #cls.admin = User.objects.create_superuser(username="admin", email="admin@admin.com", password="supersafepassword")
        #Create users
        username = 'us'
        email = 'medo@testemail.com'
        password = 'thispasswordisbad'
        club_name ="hjh"
        user_type = 1

        cls.user = get_user_model().objects.create_user(
            username =username,
            email=email,
            password=password,
            club_name = club_name,
            student_id = "9234",
            user_type = user_type,
            first_name = "john"
           
        )


    def setUp(self):
        self.client = APIClient()

    def post_request(self):
        url = reverse('register')
        self.response = self.client.post(url, data={'username': 'bill',  'email': 'shdhsd',
            'password': 'password',
            'club_name' : 'club_name',
            'student_id' : "9234",
            'user_type' : 1,
            'first_name' : "john" })

        #Post request
        #data = self.response.data 
        #data['username'] = "someone"

    def test_successful_user_created(self): 
        self.client.login(username=self.user.username, email = self.user.email, password=self.user.password)
        self.post_request()
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
