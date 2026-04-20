from django.urls import path
from .views import LocationDataView,ScoreCalculationView
urlpatterns = [
    path('map',LocationDataView.as_view()),
    path('calculate',ScoreCalculationView.as_view())
]