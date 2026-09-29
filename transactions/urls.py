from django.urls import path
from .views import TransactionListView, DailySummaryView

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('daily-summary/', DailySummaryView.as_view(), name='daily-summary'),
]