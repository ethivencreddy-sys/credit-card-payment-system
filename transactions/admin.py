import csv

from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone
from django.urls import path

from .models import Transaction


def export_transactions_csv(modeladmin, request, queryset):
    response = HttpResponse(
        content_type='text/csv'
    )
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'ID',
        'Transaction Reference',
        'User',
        'Card',
        'Amount',
        'Status',
        'Created At',
        'Updated At',
    ])

    for transaction in queryset:
        writer.writerow([
            transaction.id,
            transaction.transaction_reference,
            transaction.user.username,
            transaction.card.last_four_digits,
            transaction.amount,
            transaction.status,
            transaction.created_at,
            transaction.updated_at,
        ])

    return response


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'transaction_reference',
        'user',
        'card',
        'amount',
        'status',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'transaction_reference',
        'user__username',
    )

    actions = [export_transactions_csv]

    def daily_summary(self, request):
        today = timezone.localdate()

        today_transactions = Transaction.objects.filter(
            created_at__date=today
        )

        summary = today_transactions.aggregate(
            total_transactions=Count('id'),
            total_amount=Sum('amount'),
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

        return JsonResponse({
            'date': str(today),
            'total_transactions': summary['total_transactions'] or 0,
            'total_amount': str(summary['total_amount'] or 0),
            'successful': successful,
            'failed': failed,
            'pending': pending,
        })

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                'daily-summary/',
                self.admin_site.admin_view(self.daily_summary),
                name='transaction-daily-summary',
            ),
        ]

        return custom_urls + urls