from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone

from .models import Transaction
from .serializers import TransactionSerializer
class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

        status = self.request.query_params.get('status')
        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if status:
            queryset = queryset.filter(status=status.upper())

        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)

        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)

        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)

        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset
class DailySummaryView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()

        today_transactions = Transaction.objects.filter(
            created_at__date=today
        )

        summary = today_transactions.aggregate(
            total_transactions=Count('id'),
            total_amount=Sum('amount')
        )

        successful = today_transactions.filter(
            status='SUCCESS'
        ).count()

        failed = today_transactions.filter(
            status='FAILED'
        ).count()

        pending = today_transactions.filter(
            status='PENDING'
        ).count()

        return Response({
            "date": str(today),
            "total_transactions": summary["total_transactions"] or 0,
            "total_amount": str(summary["total_amount"] or 0),
            "successful": successful,
            "failed": failed,
            "pending": pending
        })