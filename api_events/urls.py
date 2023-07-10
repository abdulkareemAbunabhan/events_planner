from django.urls import path
from .views import EventsDataView,WeatherDataView,FlightsDataView


urlpatterns = [
    path('<str:country>/', EventsDataView.as_view(), name='events_list'),
    path('weather/<str:event_id>/', WeatherDataView.as_view(), name='weather_list'),
    path('flight/<str:event_id>/<str:user_airport_iata_code>/',FlightsDataView.as_view(),name='flights_list')
]