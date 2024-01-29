from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
import json
from ..models import StockData, User, Transaction
from unittest.mock import patch, MagicMock


class testTransaction(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='TEST', balance='400.0')
        self.stockdata = {
            'ticker': 'TEST',
            'open_price': '10.0',
            'close_price': '12.0',
            'high': '13.0',
            'low': '10.0',
            'volume': '10',
            'timestamp': '2024-01-26T15:30:00Z'
        }
        self.stock = StockData.objects.create(**self.stockdata)
        self.transaction = {
            'ticker': self.stock.id,
            'user_id': str(self.user.user_id),
            'transaction_type': 'buy',
            'transaction_volume': '10'
        }
        self.data = json.dumps(self.transaction)

    @patch('api.views.processing_transaction.delay')
    @patch('api.views.AsyncResult')
    def test_create_transaction(self, celery_val, celery_result):
        celery_result.return_value = MagicMock(id='mocked_task_id')
        celery_val.return_value = MagicMock(id='result', status='SUCCESS', result=True)
        url = 'http://127.0.0.1:8000/transactions/'
        response = self.client.post(url, data=self.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['ticker'], self.stock.id)
        self.assertEqual(response.data['data']['transaction_type'], 'buy')

    def test_retrieve_transaction_by_user(self):
        transaction = Transaction.objects.create(**self.transaction)
        user_id = transaction.user_id
        url = f'http://127.0.0.1:8000/transaction/{user_id}'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('api.views.processing_transaction.delay')
    @patch('api.views.AsyncResult')
    def test_Insuficient_balance(self, celery_val, celery_result):
        celery_result.return_value = MagicMock(id='mocked_task_id')
        celery_val.return_value = MagicMock(id='result', status='SUCCESS', result=False)
        url = 'http://127.0.0.1:8000/transactions/'
        response = self.client.post(url, data=self.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Error'], 'Balance is less for this transaction.------')
