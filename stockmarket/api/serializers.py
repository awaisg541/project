from rest_framework import serializers
from .models import User, StockData, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'balance')
        read_only_fields = ['user_id']

    def validate(self, data):
        if data['balance'] <= 0:
            raise serializers.ValidationError('Balance cannot be less than 0.')
        if data['username'] != data['username'].upper():
            raise serializers.ValidationError('Username should be uppercase.')
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        # fields = '__all__'
        exclude = ('id',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user_id', 'ticker', 'transaction_type', 'transaction_volume']

