import os
import sys
import random
from datetime import datetime
from decimal import Decimal

import django
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Add the Django project root to Python's path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from cards.models import Card
from transactions.models import Transaction


app = FastAPI(
    title="Credit Card Payment API",
    description="Payment processing service for the Credit Card Payment System",
    version="1.0.0"
)


class PaymentRequest(BaseModel):
    user_id: int
    card_id: int
    amount: float = Field(gt=0)


@app.get("/")
def home():
    return {"message": "Credit Card Payment API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/payments/")
def make_payment(payment: PaymentRequest):

    # Check that the user exists
    try:
        user = User.objects.get(id=payment.user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found.")

    # Check that the card belongs to the user
    try:
        card = Card.objects.get(
            id=payment.card_id,
            user=user
        )
    except Card.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Card not found or does not belong to the user."
        )

    # Create transaction with initial PENDING status
    transaction = Transaction.objects.create(
        user=user,
        card=card,
        amount=Decimal(str(payment.amount)),
        status="PENDING",
        transaction_reference=f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    )

    # Simulate payment processing
    success = random.choice([True, False])

    if success:
        transaction.status = "SUCCESS"
    else:
        transaction.status = "FAILED"

    transaction.save()

    return {
        "transaction_id": transaction.id,
        "transaction_reference": transaction.transaction_reference,
        "user_id": transaction.user.id,
        "card_id": transaction.card.id,
        "amount": float(transaction.amount),
        "initial_status": "PENDING",
        "status": transaction.status,
        "processed_at": transaction.updated_at
    }