from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Card
from .serializers import CardSerializer


class CardListCreateView(generics.ListCreateAPIView):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        card_number = data.get("card_number")

        if not card_number:
            return Response(
                {"error": "Card number is required."},
                status=400
            )

        card_number = str(card_number).replace(" ", "")

        if not card_number.isdigit() or len(card_number) < 13:
            return Response(
                {"error": "Invalid card number."},
                status=400
            )

        data["masked_card_number"] = "*" * (len(card_number) - 4) + card_number[-4:]
        data["last_four_digits"] = card_number[-4:]

        data.pop("card_number", None)
        data.pop("cvv", None)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            masked_card_number=data["masked_card_number"],
            last_four_digits=data["last_four_digits"]
        )

        return Response(serializer.data, status=201)
        return Response(serializer.data, status=201)


class CardDeleteView(generics.DestroyAPIView):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)