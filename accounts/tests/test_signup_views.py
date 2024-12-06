from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.views import SignUpView
from accounts.forms import CustomUserCreationForm
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model


class SignUpTest(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)


    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEquals(view.func.view_class, SignUpView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)

class SuccessSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'email': 'john@gmail.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.signin_url = reverse('signin')

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to the signin page
        '''
        self.assertRedirects(self.response, self.signin_url)

    def test_user_creation(self):
        self.assertTrue(get_user_model().objects.exists())

    # def test_user_authentication(self):
    #     '''
    #     Create a new request to an arbitrary page.
    #     The resulting response should now have a `user` to its context,
    #     after a successful sign up.
    #     '''
    #     response = self.client.get(self.signin_url)
    #     user = response.context.get('user')
    #     self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})


    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        print(form.errors)
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(get_user_model().objects.exists())