from rest_framework.test import APIClient, APITestCase
from rest_framework import status

# Create your tests here.

class UserRegisterAPITestCase(APITestCase):
    url = '/api/v1/accounts/register/'
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_by_invite(self):
        resp = self.client.post(
            self.url, 
            data={'email': 'dev@ya.ru', 'password': '1234567a', 'password_repeat': '1234567a', 'email_interloc': 'dev1@ya.ru'}
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post(
            self.url,
            data={'email': 'dev1@ya.ru', 'password': '1234567a', 'password_repeat': '1234567a', 'email_interloc': 'dev@ya.ru'}
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_another_invite(self):
        resp = self.client.post(
            self.url, 
            data={'email': 'dev@ya.ru', 'password': '1234567a', 'password_repeat': '1234567a', 'email_interloc': 'dev1@ya.ru'}
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post(
            self.url,
            data={'email': 'dev2@ya.ru', 'password': '1234567a', 'password_repeat': '1234567a', 'email_interloc': 'dev@ya.ru'}
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_user_with_same_email(self):
        resp = self.client.post(
            self.url, 
            data={'email': 'dev@ya.ru', 'password': '1234567a', 'password_repeat': '1234567a', 'email_interloc': 'dev1@ya.ru'}
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post(
            self.url, 
            data={'email': 'dev@ya.ru', 'password': '1234567a', 'password_repeat': '1234567a', 'email_interloc': 'dev1@ya.ru'}
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_with_interloc_in_another_chat(self):
        resp = self.client.post(
            self.url, 
            data={'email': 'dev@ya.ru', 'password': '1234567a', 'password_repeat': '1234567a', 'email_interloc': 'dev1@ya.ru'}
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post(
            self.url, 
            data={'email': 'dev1@ya.ru', 'password': '1234567a', 'password_repeat': '1234567a', 'email_interloc': 'dev2@ya.ru'}
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.post(
            self.url, 
            data={'email': 'dev1@ya.ru', 'password': '1234567a', 'password_repeat': '1234567a', 'email_interloc': 'dev@ya.ru'}
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post(
            self.url, 
            data={'email': 'dev2@ya.ru', 'password': '1234567a', 'password_repeat': '1234567a', 'email_interloc': 'dev1@ya.ru'}
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)



class UserRefreshPasswordAPITestCase(APITestCase):

    url = '/api/v1/accounts/refresh_password/'

    def setUp(self):
        self.client = APIClient()

        self.invite_email = 'dev1@ya.ru'
        self.client.post(
            '/api/v1/accounts/register/', 
            data={'email': 'dev@ya.ru', 'password': '1234567a', 'password_repeat': '1234567a', 'email_interloc': self.invite_email}
        )
    
    def test_refresh_for_invited_user(self):
        resp = self.client.post(self.url, data={'email': self.invite_email})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_not_registered_user(self):
        resp = self.client.post(self.url, data={'email': 'dev123@ya.ru'})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registered_user(self):
        resp = self.client.post(self.url, data={'email': 'dev@ya.ru'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)