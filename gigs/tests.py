"""
Tests for mfweb application.
"""
import datetime
import re
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.utils.unittest import skip

from gigs.models import Gig

"""
Behaviour Tests
"""


class AdminTests(TestCase):
    """
    Behaviour tests for the admin system
    """

    def setUp(self):
        self.test_user_name = 'testuser'
        self.test_email = 'test@test.com'
        self.test_password = 'testpassword'

        self.test_user = User.objects.create_user(
            self.test_user_name,
            self.test_email,
            self.test_password
        )

    def tearDown(self):
        self.test_user.delete()

    def test_can_view_admin_log_in(self):
        """
        Tests that we can view the admin login page
        """
        response = self.client.get(reverse('gigs:login'))
        self.assertEqual(response.status_code, 200)

    def test_can_log_in(self):
        """
        Tests that a user can log in
        """
        response = self.client.post(
            reverse('gigs:login'),
            {'username': self.test_user_name, 'password': self.test_password}
        )
        self.assertEqual(response.status_code, 302)

    def test_cannot_log_in_with_bad_password(self):
        """
        Tests that a user cannot log in with a bad password
        """
        response = self.client.post(
            reverse('gigs:login'),
            {self.test_user_name: 'testuser', 'password': 'wibble'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(re.search(b'no not match', response.content))

    def test_cannot_view_admin_index_without_login(self):
        """
        Ensure that a client which is not logged in cannot view the admin index
        """
        response = self.client.get(reverse('gigs:admin'))
        self.assertEqual(response.status_code, 302)

    @skip("Skipping tra la la")
    def test_can_view_add_gig_with_login(self):
        """
        Ensure that a logged in client can view the add gigs screen
        """
        result = self.client.login(
            username=self.test_user_name,
            password=self.test_password
        )

        self.assertTrue(result)

        response = self.client.get(reverse('gigs:add_gig'))
        self.assertEqual(response.status_code, 200)

"""
Unit Tests
"""


class GigModelTests(TestCase):
    """
    Unit tests for the gig model and the gig model manager
    """
    def test_can_instantiate(self):
        """
        Ensure we can instantiate the gig model
        """
        gig = Gig()
        self.assertIsInstance(gig, Gig)

    def test_is_valid_with_valid_values(self):
        """
        Ensure that a gig instance validates with valid values
        """

        gig = Gig(
            title='wibble',
            date=timezone.now() + datetime.timedelta(days=1)
        )
        gig.full_clean()

    def test_is_valid_with_optional_url(self):
        """
        Ensure that a gig with a url set validates
        """
        gig = Gig(
            title='wibble',
            date=timezone.now() + datetime.timedelta(days=1),
            url='http://www.google.com'
        )
        gig.full_clean()

    def test_invalid_with_blank_title(self):
        """
        Ensure validation fails if the title is missing
        """
        gig = Gig(date=timezone.now() + datetime.timedelta(days=1))
        self.assertRaises(ValidationError, gig.full_clean)

    def test_invalid_with_blank_date(self):
        """
        Ensure validation fails if the date is missing
        """
        gig = Gig(title="wibble")
        self.assertRaises(ValidationError, gig.full_clean)

    def test_invalid_with_malformed_url(self):
        """
        Ensure validation fails with a malformed url
        """
        gig = Gig(
            title="wibble",
            date=timezone.now() + datetime.timedelta(days=1),
            url='iamabadurl'
        )
        self.assertRaises(ValidationError, gig.full_clean)
