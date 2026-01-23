from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction as db_transaction

from .models import Transaction
from .serializers import TransactionSerializer
from wallet.models import Wallet

class TransactionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        wallet, _ = Wallet.objects.get_or_create(user=user)

        amount = serializer.validated_data['amount']
        txn_type = serializer.validated_data['transaction_type']

        # 🔐 Atomic operation (VERY IMPORTANT)
        with db_transaction.atomic():
            if txn_type == 'EXPENSE' and wallet.balance < amount:
                return Response(
                    {"error": "Insufficient balance"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update wallet balance
            if txn_type == 'INCOME':
                wallet.balance += amount
            else:
                wallet.balance -= amount

            wallet.save()

            # Save transaction
            Transaction.objects.create(
                user=user,
                wallet=wallet,
                **serializer.validated_data
            )

        return Response(
            {"message": "Transaction added successfully"},
            status=status.HTTP_201_CREATED
        )

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionListView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user
        ).order_by('-created_at')
