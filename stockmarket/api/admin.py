from django.contrib import admin
from .models import StockData, User, Transaction


# Register your models here.
@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ticker', 'open_price']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_id']


@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    list_display = ['transaction_id']
