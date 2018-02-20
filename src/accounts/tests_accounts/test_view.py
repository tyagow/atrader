from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase


class RegisterTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('accounts:register'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'registration/registration_form.html')
    
    def test_post_form(self):
        data = dict(password='teste', email='tyago@email.com', email2='')
    

class LoginTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('accounts:login'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'registration/login.html')


class SettingsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "user123",
            "user@example.com",
            "password123")

    def test_get(self):
        self.assertTrue(self.client.login(username='user123', password='password123'))

        self.response = self.client.get(r('accounts:settings'))

        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use registration/settings.html"""

        self.assertTrue(self.client.login(username='user123', password='password123'))

        self.response = self.client.get(r('accounts:settings'))
        self.assertTemplateUsed(self.response, 'accounts/settings.html')

