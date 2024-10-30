from django.test import TestCase
from django.urls import reverse, resolve
from accounts import views


class TestUrls(TestCase):
    def test_login_view(self):
        url = reverse('accounts:user_login')
        self.assertEqual(resolve(url).func.view_class, views.UserLoginView)

    def test_logout_view(self):
        url = reverse('accounts:user_logout')
        self.assertEqual(resolve(url).func.view_class, views.UserLogoutView)

    def test_register_view(self):
        url = reverse('accounts:user_register')
        self.assertEqual(resolve(url).func.view_class, views.UserRegisterView)

    def test_verify_view(self):
        url = reverse('accounts:user_register_verify_code')
        self.assertEqual(resolve(url).func.view_class, views.UserRegisterVerifyCodeView)

