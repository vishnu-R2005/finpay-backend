from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Bill
from .serializers import BillSerializer

class BillListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bills = Bill.objects.filter(user=request.user).order_by('due_date')
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BillDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        bill = Bill.objects.get(pk=pk, user=request.user)
        serializer = BillSerializer(bill, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        bill = Bill.objects.get(pk=pk, user=request.user)
        bill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
