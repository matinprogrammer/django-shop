from django.test import TestCase
from accounts import models
import datetime
import pytz

class TestOtpCodeModel(TestCase):

    def setUp(self):
        otp_code = models.OtpCode.objects.create(phone_number='09000000000', code='123456')
        self.created = datetime.datetime.now(tz=pytz.timezone('Asia/Tehran'))
        otp_code.created = self.created
        otp_code.save()
        self.otp_code = otp_code

    def test_model_str(self):
        self.assertEqual(str(self.otp_code), f'09000000000 - 123456 - {self.created}')

class TestUserModel(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(
            phone_number='09000000000',
            first_name='test',
            password='test_pass'
        )
    def test_model_str(self):
        self.assertEqual(str(self.user), '09000000000')


