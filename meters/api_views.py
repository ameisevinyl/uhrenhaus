from rest_framework import generics, permissions
from .models import Meter, MeterReading, Unit, ConsumptionType, Expense
from .serializers import MeterSerializer, MeterReadingSerializer, UnitSerializer, ConsumptionTypeSerializer, ExpenseSerializer

# ✅ Meters API
class MeterListView(generics.ListCreateAPIView):
    """List all meters or create a new meter"""
    queryset = Meter.objects.all()
    serializer_class = MeterSerializer
    permission_classes = [permissions.IsAuthenticated]

class MeterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific meter"""
    queryset = Meter.objects.all()
    serializer_class = MeterSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Meter Readings API
class MeterReadingListView(generics.ListCreateAPIView):
    """List all meter readings or create a new one"""
    queryset = MeterReading.objects.all()
    serializer_class = MeterReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Assign the logged-in user when creating a new meter reading"""
        serializer.save(user=self.request.user)

class MeterReadingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific meter reading"""
    queryset = MeterReading.objects.all()
    serializer_class = MeterReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Units API
class UnitListView(generics.ListAPIView):
    """List all units"""
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]

class UnitDetailView(generics.RetrieveAPIView):
    """Retrieve a specific unit"""
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Consumption Types API
class ConsumptionTypeListView(generics.ListAPIView):
    """List all consumption types"""
    queryset = ConsumptionType.objects.all()
    serializer_class = ConsumptionTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Expenses API
class ExpenseListView(generics.ListCreateAPIView):
    """List all expenses or create a new one"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific expense"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
