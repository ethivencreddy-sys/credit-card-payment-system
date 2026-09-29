from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Card


class CardTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="carduser",
            password="TestPassword123"
        )

        self.client.force_authenticate(user=self.user)

    def test_create_card(self):
        data = {
            "card_type": "CREDIT",
            "card_holder_name": "Card User",
            "card_number": "4111111111111111",
            "expiry_month": 12,
            "expiry_year": 2030
        }

        response = self.client.post(
            "/api/cards/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["last_four_digits"], "1111")
        self.assertEqual(
            response.data["masked_card_number"],
            "************1111"
        )

        self.assertEqual(Card.objects.count(), 1)

    def test_list_cards(self):
        Card.objects.create(
            user=self.user,
            card_type="CREDIT",
            card_holder_name="Card User",
            masked_card_number="************1111",
            last_four_digits="1111",
            expiry_month=12,
            expiry_year=2030
        )

        response = self.client.get("/api/cards/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_card(self):
        card = Card.objects.create(
            user=self.user,
            card_type="CREDIT",
            card_holder_name="Card User",
            masked_card_number="************1111",
            last_four_digits="1111",
            expiry_month=12,
            expiry_year=2030
        )

        response = self.client.delete(
            f"/api/cards/{card.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Card.objects.filter(id=card.id).exists()
        )