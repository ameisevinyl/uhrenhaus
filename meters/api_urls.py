from django.urls import path
from .api_views import (
    MeterListView, MeterDetailView, MeterReadingListView, MeterReadingDetailView,
    UnitListView, UnitDetailView, ConsumptionTypeListView, ExpenseListView, ExpenseDetailView
)

urlpatterns = [
    path("meters/", MeterListView.as_view(), name="meter-list"),
    path("meters/<int:pk>/", MeterDetailView.as_view(), name="meter-detail"),

    path("meter-readings/", MeterReadingListView.as_view(), name="meter-reading-list"),
    path("meter-readings/<int:pk>/", MeterReadingDetailView.as_view(), name="meter-reading-detail"),

    path("units/", UnitListView.as_view(), name="unit-list"),
    path("units/<int:pk>/", UnitDetailView.as_view(), name="unit-detail"),

    path("consumption-types/", ConsumptionTypeListView.as_view(), name="consumption-type-list"),

    path("expenses/", ExpenseListView.as_view(), name="expense-list"),
    path("expenses/<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail"),
]
