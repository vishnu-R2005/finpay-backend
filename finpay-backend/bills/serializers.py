from rest_framework import serializers
from .models import Bill

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = [
            'id',
            'title',
            'amount',
            'bill_type',
            'due_date',
            'is_paid',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
