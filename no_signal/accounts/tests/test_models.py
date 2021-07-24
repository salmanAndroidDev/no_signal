from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data = {'email': 'email@gmail.com',
                    'password': "pass1234"}

    def test_create_user_successfully(self):
        """Test create user by email and password"""
        data = self.data
        user = User.objects.create_user(**data)
        self.assertEqual(data['email'], user.email)
        self.assertTrue(user.check_password(data['password']))

    def test_make_new_user_email_normalized(self):
        """Test make new user email normalized"""
        data = self.data
        data['email'] = "salman@GMAIL.COME"
        user = User.objects.create_user(**self.data)

        self.assertEqual(user.email, data['email'].lower())

    def test_make_user_invalid_email(self):
        """Test raise error if email is not valid"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None,
                                     password="test1234")

    def test_create_super_user(self):
        "Test creating a new super user"
        user = User.objects.create_superuser(**self.data)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
