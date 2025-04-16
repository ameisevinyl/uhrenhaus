from rest_framework import serializers
from .models import Meter, MeterReading, Unit, ConsumptionType, Expense

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"

class ConsumptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumptionType
        fields = "__all__"

class MeterSerializer(serializers.ModelSerializer):
    """Serialize Meter objects including related data."""
    consumption_type = ConsumptionTypeSerializer(read_only=True)
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = Meter
        fields = "__all__"

class MeterReadingSerializer(serializers.ModelSerializer):
    """Serialize meter readings including meter info."""
    meter = MeterSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MeterReading
        fields = "__all__"

class ExpenseSerializer(serializers.ModelSerializer):
    """Serialize expenses including meter readings and related info."""
    meter = MeterSerializer(read_only=True)
    start_reading = MeterReadingSerializer(read_only=True)
    end_reading = MeterReadingSerializer(read_only=True)
    supplier = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Expense
        fields = "__all__"
