from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from cards.models import Card
from .models import Transaction


class TransactionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="paymentuser",
            password="TestPassword123"
        )

        self.card = Card.objects.create(
            user=self.user,
            card_type="CREDIT",
            card_holder_name="Payment User",
            masked_card_number="************1111",
            last_four_digits="1111",
            expiry_month=12,
            expiry_year=2030
        )

        self.client.force_authenticate(user=self.user)

    def test_transaction_history(self):
        Transaction.objects.create(
            user=self.user,
            card=self.card,
            amount=500.00,
            status="SUCCESS",
            transaction_reference="TEST-TXN-001"
        )

        response = self.client.get("/api/transactions/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "SUCCESS")

    def test_transaction_status_filter(self):
        Transaction.objects.create(
            user=self.user,
            card=self.card,
            amount=500.00,
            status="SUCCESS",
            transaction_reference="TEST-TXN-002"
        )

        Transaction.objects.create(
            user=self.user,
            card=self.card,
            amount=250.00,
            status="FAILED",
            transaction_reference="TEST-TXN-003"
        )

        response = self.client.get(
            "/api/transactions/?status=SUCCESS"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "SUCCESS")

    def test_daily_summary(self):
        Transaction.objects.create(
            user=self.user,
            card=self.card,
            amount=500.00,
            status="SUCCESS",
            transaction_reference="TEST-TXN-004"
        )

        response = self.client.get(
            "/api/transactions/daily-summary/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_transactions"], 1)
        self.assertEqual(response.data["successful"], 1)