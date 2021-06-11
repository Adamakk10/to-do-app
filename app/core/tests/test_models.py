from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_with_email(self):
        """test creating user with email instead of username"""
        email = 'test@gmail.com'
        password = 'test1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_is_normalized(self):
        """test that users email is normalized"""

        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test1234')

        self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        """test that user has entered invalid email"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')

    def test_create_superuser(self):
        """test creating superuser"""
        user = get_user_model().objects.create_superuser(
            email='test@gmail.com',
            password='test1234'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
