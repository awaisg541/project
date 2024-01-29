from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
import json

from ..models import StockData


class testStock(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.stock = {
            'ticker': 'TEST',
            'open_price': '10.00',
            'close_price': '12.00',
            'high': '13.00',
            'low': '10.00',
            'volume': '10',
            'timestamp': '2022-01-25 15:30:00'
        }
        self.data = json.dumps(self.stock)

    def test_create_stock(self):
        url = 'http://127.0.0.1:8000/stocks/'
        response = self.client.post(url, data=self.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_stock(self):
        stock = StockData.objects.create(**self.stock)
        url = 'http://127.0.0.1:8000/stocks/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['ticker'], stock.ticker)
        self.assertEqual(response.data['data'][0]['open_price'], stock.open_price)
        self.assertEqual(response.data['data'][0]['close_price'], stock.close_price)

    def test_retrieve_stock_from_cache(self):
        stock = StockData.objects.create(**self.stock)
        url = 'http://127.0.0.1:8000/stocks/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['ticker'], stock.ticker)
        self.assertEqual(response.data['data'][0]['open_price'], stock.open_price)
        self.assertEqual(response.data['data'][0]['close_price'], stock.close_price)
        self.assertEqual(response.data['msg'], 'data coming from cache')

    def test_detail_stock(self):
        stock = StockData.objects.create(**self.stock)
        url = f'http://127.0.0.1:8000/stocks/{stock.ticker}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['ticker'], stock.ticker)
