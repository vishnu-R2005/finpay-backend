from django.urls import path
from .views import TransactionCreateView

urlpatterns = [
    path('', TransactionCreateView.as_view(), name='create-transaction'),
    path('history/', TransactionListView.as_view(), name='transaction-history'),

]
