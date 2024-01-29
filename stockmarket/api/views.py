from rest_framework.response import Response
from django.core.cache import cache
from rest_framework import status
from rest_framework.views import APIView
from .tasks import processing_transaction
from .models import User, StockData, Transaction
from .serializers import UserSerializer, StockDataSerializer, TransactionSerializer
from celery.result import AsyncResult


# Create your views here.

class RegisterAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPI(APIView):
    def get(self, request, username=None):
        cache_data = cache.get(f'{username}_data')
        if not cache_data:
            try:
                user = User.objects.get(username=username)
                serializer = UserSerializer(user)
                cache.set(f'{username}_data', serializer.data, timeout=3)
                return Response({'data': serializer.data, 'msg': 'data coming from database'},
                                status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'data': cache_data, 'msg': 'data coming from cache'}, status=status.HTTP_200_OK)


class StockdataAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StockDataSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            cache.set('stock_data', serializer.data, timeout=3)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        all_stock_data = [cache.get(key) for key in cache.keys('*stock*')]
        if not all_stock_data:
            stock = StockData.objects.all()
            if stock:
                serializer = StockDataSerializer(stock, many=True)
                cache.set('stock_data', serializer.data, timeout=3)
                return Response({'data': serializer.data, 'msg': 'data coming from database'},
                                status=status.HTTP_200_OK)
            else:
                return Response('No stock data found')
        else:
            return Response({'data': all_stock_data, 'msg': 'data coming from cache'}, status=status.HTTP_200_OK)


class StockdataDetailAPI(APIView):
    def get(self, request, ticker=None):
        stock_data = cache.get(f'{ticker}_data')
        if not stock_data:
            try:
                stock = StockData.objects.get(ticker=ticker)
                serializer = StockDataSerializer(stock)
                cache.set(f'{ticker}_data', serializer.data)
                return Response({'data': serializer.data, 'msg': 'data coming from database'},
                                status=status.HTTP_200_OK)
            except StockData.DoesNotExist:
                return Response('stock not found', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'data': stock_data, 'msg': 'data coming from cache'}, status=status.HTTP_200_OK)


class TransactionAPI(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user_id']
        ticker = serializer.validated_data['ticker']
        transaction_type = serializer.validated_data['transaction_type']
        transaction_volume = serializer.validated_data['transaction_volume']
        try:
            stock = StockData.objects.filter(ticker=ticker).latest('timestamp')
        except StockData.DoesNotExist:
            return Response({'error': 'Stock does not exist'}, status=status.HTTP_404_NOT_FOUND)
        transaction_price = stock.close_price * transaction_volume

        username = user.username
        result = processing_transaction.delay(transaction_price, transaction_type, username)
        val = AsyncResult(result.id)
        while True:
            if val.status == 'SUCCESS':
                break
        if val.result:
            serializer.validated_data['transaction_price'] = transaction_price
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        elif not val.result:
            return Response({'Error': 'Balance is less for this transaction.------'},
                            status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailAPI(APIView):
    def get(self, request, user_id=None):
        transaction_data = cache.get(f'{user_id}_data')
        if not transaction_data:
            try:
                transactions = Transaction.objects.filter(user_id__user_id=user_id)
                serializer = TransactionSerializer(transactions)
                cache.set(f'{user_id}_data', serializer.data)
                return Response({'data': serializer.data, ',msg': 'data coming from database'},
                                status=status.HTTP_200_OK)
            except Transaction.DoesNotExist:
                return Response('Transaction does not exist', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'data': transaction_data, 'msg': 'data is coming from cache'}, status=status.HTTP_200_OK)


class UserTransactionDateRangeAPI(APIView):
    def get(self, request, user_id=None, start=None, end=None):
        try:
            transations = Transaction.objects.filter(user__user_id=user_id, timestamp__range=[start, end])
            serializer = TransactionSerializer(transations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({'Error': 'transaction does not exist'}, status=status.HTTP_404_NOT_FOUND)
