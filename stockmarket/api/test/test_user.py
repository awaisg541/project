from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
import json

from ..models import User


class testUser(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = {
            'username': 'TEST',
            'balance': '10.00'
        }
        self.data = json.dumps(self.user)

    def test_create_user(self):
        url = 'http://127.0.0.1:8000/users/'
        response = self.client.post(url, data=self.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.user['username'])
        self.assertEqual(response.data['balance'], self.user['balance'])

    def test_retrieve_user(self):
        user = User.objects.create(username='TESTS', balance='10.00')
        username = user.username
        url = f'http://127.0.0.1:8000/users/{username}/'
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['username'], username)
        self.assertEqual(response.data['data']['balance'], user.balance)
        self.assertEqual(response.data['msg'], 'data coming from database')

    def test_retrieve_user_from_cache(self):
        user = User.objects.create(username='TESTS', balance='10.00')
        username = user.username
        url = f'http://127.0.0.1:8000/users/{username}/'
        response1 = self.client.get(url, content_type='application/json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data['data']['username'], username)
        self.assertEqual(response1.data['data']['balance'], user.balance)
        self.assertEqual(response1.data['msg'], 'data coming from cache')

    def test_create_user_negative_balance(self):
        url = f'http://127.0.0.1:8000/users/'
        data = {'username': 'TEST', 'balance': '-10.0'}
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
