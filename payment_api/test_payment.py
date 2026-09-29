from unittest.mock import patch
from django.test import TestCase

from django.contrib.auth.models import User

from cards.models import Card
from transactions.models import Transaction

from .main import PaymentRequest, make_payment


class PaymentTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="paymentuser",
            password="TestPass123!"
        )

        self.card = Card.objects.create(
            user=self.user,
            card_type="CREDIT",
            card_holder_name="Payment User",
            masked_card_number="************1111",
            last_four_digits="1111",
            expiry_month=12,
            expiry_year=2030,
        )

    @patch("payment_api.main.random.choice", return_value=True)
    def test_successful_payment(self, mock_choice):
        payment = PaymentRequest(
            user_id=self.user.id,
            card_id=self.card.id,
            amount=500.00
        )

        response = make_payment(payment)

        self.assertEqual(response["status"], "SUCCESS")
        self.assertEqual(response["initial_status"], "PENDING")
        self.assertEqual(response["amount"], 500.0)

        transaction = Transaction.objects.get(
            id=response["transaction_id"]
        )

        self.assertEqual(transaction.status, "SUCCESS")

    @patch("payment_api.main.random.choice", return_value=False)
    def test_failed_payment(self, mock_choice):
        payment = PaymentRequest(
            user_id=self.user.id,
            card_id=self.card.id,
            amount=250.00
        )

        response = make_payment(payment)

        self.assertEqual(response["status"], "FAILED")
        self.assertEqual(response["initial_status"], "PENDING")
        self.assertEqual(response["amount"], 250.0)

        transaction = Transaction.objects.get(
            id=response["transaction_id"]
        )

        self.assertEqual(transaction.status, "FAILED")