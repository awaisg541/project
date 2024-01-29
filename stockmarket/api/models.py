from django.db import models
import uuid


# Create your models here.
class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4
                               , editable=False)
    username = models.CharField(max_length=255, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username


class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    open_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    close_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    high = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    low = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    volume = models.PositiveIntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.ticker


class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.ForeignKey(StockData, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    transaction_volume = models.PositiveIntegerField()
    transaction_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'{self.ticker} - {self.transaction_type}'


# @receiver(post_save, sender=Transaction)
# def create_transaction(sender, instance, created, **kwargs):
#     if created:
#         processing_transaction.delay(instance.transaction_id)
