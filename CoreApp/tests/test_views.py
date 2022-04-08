from django.test import TestCase, Client
from django.urls import reverse
from CoreApp.models import *
import json


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_form(self):
        response = self.client.get(reverse('login_form'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/login.html')

    def test_logoutView(self):
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)

    def test_loginView(self):
        User.objects.create_user(
            username='parvesharma',
            password='Sh$560037KA'
        )
        response = self.client.post('login')
        self.assertEquals(response.status_code, 404)
