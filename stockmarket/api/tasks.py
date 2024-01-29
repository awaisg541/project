from celery import shared_task


@shared_task
def processing_transaction(transaction_price, transaction_type, username):
    from .models import User
    user = User.objects.get(username=username)
    if transaction_type == 'buy' and user.balance < transaction_price:
        return False
    elif transaction_type == 'buy':
        user.balance -= transaction_price
        user.save()
        return True
    elif transaction_type == 'sell':
        user.balance += transaction_price
        user.save()
        return True
