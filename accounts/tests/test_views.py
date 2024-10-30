from django.test import TestCase
from accounts.models import User, OtpCode
from accounts import views, forms
from django.urls import reverse
from unittest import mock


class TestUserLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='09000000000',
            first_name='test',
            password='test_pass',
        )
        self.credential = {
            'phone_number': '09000000000',
            'password': 'test_pass'
        }

    def test_user_login_GET(self):
        response = self.client.get(reverse('accounts:user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_login.html')
        self.failUnless(response.context['form'], forms.UserLoginForm)

    def test_user_login_POST_valid(self):
        response = self.client.post(reverse('accounts:user_login'), self.credential)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))

    def test_user_login_POST_invalid(self):
        response = self.client.post(reverse('accounts:user_login'), {
            'phone_number': '09000000000',
            'password': 'invalid-pass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_login.html')
        self.failUnless(response.context['form'], forms.UserLoginForm)


class TestUserLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='09000000000',
            first_name='test',
            password='test_pass',
        )
        self.credential = {
            'phone_number': '09000000000',
            'password': 'test_pass'
        }

    def test_user_logout_GET(self):
        self.client.login(**self.credential)
        response = self.client.get(reverse('accounts:user_logout'))
        self.assertFalse(hasattr(response.request, 'user'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))


class UserRegisterView(TestCase):
    def test_user_register_GET(self):
        response = self.client.get(reverse('accounts:user_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_register.html')
        self.failUnless(response.context['form'], forms.UserRegisterForm)

    @mock.patch('accounts.views.send_otp_code')
    def test_user_register_POST_valid(self, mock_send_otp_code):
        response = self.client.post(reverse('accounts:user_register'), {
            'phone_number': '09000000000',
            'first_name': 'test',
            'password1': 'test_pass',
            'password2': 'test_pass',
        })
        session = self.client.session[views.USER_REGISTER_SESSION_KEY]

        self.assertEqual(OtpCode.objects.all().count(), 1)
        self.assertEqual(session, {
            'phone_number': '09000000000',
            'first_name': 'test',
            'last_name': None,
            'birth_date': None,
            'password': 'test_pass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:user_register_verify_code'))

    @mock.patch('accounts.views.send_otp_code')
    def test_user_register_POST_invalid(self, mock_send_otp_code):
        response = self.client.post(reverse('accounts:user_register'), {
            'phone_number': 'invalid_phone_number',
            'first_name': 'test',
            'password1': 'test_pass',
            'password2': 'example_pass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_register.html')
        self.failUnless(response.context['form'], forms.UserRegisterForm)


class UserRegisterVerifyCodeView(TestCase):
    def setUp(self):
        OtpCode.objects.create(phone_number='09000000000', code='123456')
        self.credential = {
            'phone_number': '09000000000',
            'first_name': 'test',
            'last_name': None,
            'birth_date': None,
            'password': 'test_pass'
        }

    def test_user_register_verify_code_GET(self):
        response = self.client.get(reverse('accounts:user_register_verify_code'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_register_verify_code.html')
        self.failUnless(response.context['form'], forms.VerifyCodeForm)

    def test_user_register_verify_code_POST_valid(self):
        my_session = self.client.session
        my_session[views.USER_REGISTER_SESSION_KEY] = self.credential
        my_session.save()
        response = self.client.post(reverse('accounts:user_register_verify_code'), {'code': '123456'})

        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(OtpCode.objects.all().count(), 0)
        self.assertRedirects(response, reverse('home:home'))

    def test_user_register_verify_code_POST_invalid_code(self):
        my_session = self.client.session
        my_session[views.USER_REGISTER_SESSION_KEY] = self.credential
        my_session.save()
        response = self.client.post(reverse('accounts:user_register_verify_code'), {'code': '000000'})

        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(OtpCode.objects.all().count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_register_verify_code.html')
        self.failUnless(response.context['form'], forms.VerifyCodeForm)

