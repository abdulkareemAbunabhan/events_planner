from rest_framework import serializers
from .models import Event,Weather,Flight

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields = ('event_name', 'event_id', 'event_date', 'event_lat', 'event_lon', 'desc','event_country')

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Weather
        fields = ('event_name', 'event_id','event_Temperature','event_Humidity')

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model=Flight
        fields = ('event_name','event_id', 'flights_arriving', 'flights_departing')