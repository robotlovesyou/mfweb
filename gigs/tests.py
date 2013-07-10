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
#from django.utils.unittest import skip

from gigs.models import Gig

"""
View Tests
"""


class PublicTests(TestCase):
    """
    Tests for the public facing site
    """

    def test_can_load_gigs_home(self):
        """
        Test that the gigs home page loads
        """
        response = self.client.get(reverse('gigs:home'))
        self.assertEqual(response.status_code, 200)


class AdminTests(TestCase):
    """
    View tests for the admin system
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

    def login_test_client(self):
        """
        Log in the test client using the test user
        """
        result = self.client.login(
            username=self.test_user_name,
            password=self.test_password
        )

        self.assertTrue(result)

    def create_test_gig(self):
        """
        Gig test fixture
        """
        return Gig.objects.create_gig(
            'wibble',
            timezone.now() + datetime.timedelta(days=1)
        )

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

    def test_can_view_admin_index(self):
        """
        Tests that a logged in user can view the admin index
        """
        self.login_test_client()
        response = self.client.get(reverse('gigs:admin'))
        self.assertEqual(response.status_code, 200)

    def test_can_view_add_gig_with_login(self):
        """
        Ensure that a logged in client can view the add gigs screen
        """
        self.login_test_client()

        response = self.client.get(reverse('gigs:admin_create'))
        self.assertEqual(response.status_code, 200)

    def test_cannot_view_add_gig_without_login(self):
        """
        Ensure that a client who is not logged in cannot view
        the add gigs screen
        """
        response = self.client.get(reverse('gigs:admin_create'))
        self.assertEqual(response.status_code, 302)

    def test_can_create_a_gig_with_a_login(self):
        """
        Ensure that a login is required to create a gig
        """
        self.login_test_client()
        response = self.client.post(
            reverse('gigs:admin_create'),
            {'title': 'wibble', 'date': '01/01/2050'}
        )
        self.assertEqual(response.status_code, 302)

    def test_cannot_create_a_gig_with_invalid_data(self):
        """
        Ensure that invalid gig data causes the screen to display
        an error
        """
        self.login_test_client()
        response = self.client.post(
            reverse('gigs:admin_create'),
            {'title': 'wibble', 'date': 'wibble'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search(b'Enter a valid date', response.content))

    def test_can_view_edit_gig_with_login(self):
        """
        Ensure that the edit screen for a gig can be viewed by a logged
        in user
        """
        gig = self.create_test_gig()
        self.login_test_client()
        response = self.client.get(reverse(
            'gigs:admin_update',
            kwargs={'pk': gig.pk}
        ))

        self.assertEqual(response.status_code, 200)

    def test_cannot_view_edit_gig_without_login(self):
        """
        Ensure that the gig edit screen requires a login
        """
        gig = self.create_test_gig()
        response = self.client.get(reverse(
            'gigs:admin_update',
            kwargs={'pk': gig.pk}
        ))

        self.assertEqual(response.status_code, 302)

    def test_can_edit_gig(self):
        """
        Ensure we can edit a gig
        """
        gig = self.create_test_gig()
        response = self.client.post(
            reverse('gigs:admin_update', kwargs={'pk': gig.pk}),
            {'pk': gig.pk, 'title': 'Big Boots', 'date': gig.date}
        )
        self.assertTrue(response.status_code, 302)

    def test_can_view_delete_gig(self):
        """
        Ensure the gig delete page is visible to logged in users
        """
        gig = self.create_test_gig()
        self.login_test_client()
        response = self.client.get(
            reverse('gigs:admin_delete', kwargs={'pk': gig.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_cannot_view_delete_gig_without_authentication(self):
        """
        Ensure that unauthenticated users cannot view the delete gig page
        """
        gig = self.create_test_gig()
        response = self.client.get(
            reverse('gigs:admin_delete', kwargs={'pk': gig.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_can_delete_gig(self):
        gig = self.create_test_gig()
        self.login_test_client()
        response = self.client.post(
            reverse('gigs:admin_delete', kwargs={'pk': gig.pk}),
            {}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRaises(Gig.DoesNotExist, Gig.objects.get, pk=gig.pk, deleted=False)


"""
Model Tests
"""


class GigModelTests(TestCase):
    """
    Model tests for the gig model and the gig model manager
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

    def test_can_create_gig_with_gig_manager(self):
        """
        Ensure that the gig manager create_gig method
        creates a gig
        """
        gig = Gig.objects.create_gig(
            'wibble', timezone.now() + datetime.timedelta(days=1)
        )
        self.assertIsInstance(gig, Gig)
        self.assertNotEqual(gig.pk, None)

    def test_can_mark_gig_deleted(self):
        """
        Ensure that a gig can be marked as deleted
        """
        gig = Gig.objects.create_gig(
            'wibble', timezone.now() + datetime.timedelta(days=1)
        )
        gig.delete()
        gig_from_db = Gig.objects.get(pk=gig.pk)
        self.assertTrue(gig_from_db.deleted)
