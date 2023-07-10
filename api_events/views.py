from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime, timedelta
import requests
from .models import Event,Weather,Flight
from .serializers import EventSerializer,WeatherSerializer,FlightSerializer
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404


class EventsDataView(generics.ListAPIView):
    api_url = "https://api.predicthq.com/v1/events/"
    api_key = "EqpJf87ypBIW6cbbhkXRj_HOyxkNezMRw66NdI86"
    params={"sort":"local_rank"}
    queryset = Event.objects.all()
    # serializer_class = EventSerializer
    def get(self, request,*args,**kwargs):
        country=self.kwargs.get('country')
        self.params['country']=country
        db=Event.objects.filter(event_country=country)
        current_time = timezone.now()
        if (len(db)>0 and (current_time - db[0].created_at) > (timedelta(hours=6)))or len(db)<1:
            Event.objects.filter(event_country=country).delete()
            # Retrieve data from the API
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(self.api_url, headers=headers,params=self.params)
            data = response.json()['results']
            # Store data in the model
            for item in data:
                Event.objects.create(event_name=item['title'], event_id=item['id'],event_date=item['start'],event_lat=item['location'][1],event_lon=item['location'][0],event_country=country,desc=item['description'])

            # Retrieve filtered objects
            queryset = Event.objects.filter(event_country=country)

            # Serialize the queryset
            serializer = EventSerializer(queryset, many=True)

            # Return serialized data
            return Response(serializer.data)
        else:
            queryset = Event.objects.filter(event_country=country)
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data)
        
        

class WeatherDataView(generics.ListAPIView):
    api_url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "f22892654725839a44ff6db985f0b151"
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('event_id')
        the_event = get_object_or_404(Event, event_id=id)
        print(the_event.event_lat)
        print(the_event.event_lon)
        db = Weather.objects.filter(event_id=id)
        current_time = timezone.now()
        if len(db) > 0 and (current_time - db[0].created_at) > timedelta(hours=6) or len(db) < 1:
            Weather.objects.filter(event_id=id).delete()
            # Retrieve data from the API
            self.api_url = f"{self.api_url}?lat={the_event.event_lat}&lon={the_event.event_lon}&appid={self.api_key}"
            response = requests.get(self.api_url)
            data = response.json()['main']
            # Store data in the model
            Weather.objects.create(event_name=the_event.event_name, event_id=id, event_Temperature=data['temp'], event_Humidity=data['humidity'])

            # Retrieve filtered object
            queryset = Weather.objects.get(event_id=id)

            # Serialize the queryset
            serializer = WeatherSerializer(queryset)

            # Return serialized data
            return Response(serializer.data)
        else:
            queryset = Weather.objects.get(event_id=id)
            serializer = WeatherSerializer(queryset)
            return Response(serializer.data)
          
class FlightsDataView(generics.ListAPIView):
    queryset=Flight.objects.all()
    url="https://airlabs.co/api/v9/nearby"
    api_key="24fecd28-8bc9-4f87-9778-15688f2f1963"
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('event_id')
        iata_code= self.kwargs.get('user_airport_iata_code')
        the_event = get_object_or_404(Event, event_id=id)
        db = Flight.objects.filter(event_id=id)
        current_time = timezone.now()
        if (len(db) > 0 and (current_time - db[0].created_at) > timedelta(hours=6)) or len(db) < 1:
            Flight.objects.filter(event_id=id).delete()
            # Retrieve data from the API
            print(the_event.event_lat)
            print(the_event.event_lon)
            print(self.api_key)
            self.url = f"{self.url}?lat={the_event.event_lat}&lng={the_event.event_lon}&distance=200&api_key={self.api_key}"
            response = requests.get(self.url)
            data = response.json()['response']['airports']
            print(data)
            # Store data in the model arriving part
            sorted_airports = sorted(data, key=lambda x: x["distance"])
            user_iata=iata_code
            schedule_url="https://airlabs.co/api/v9/schedules"
            for item in sorted_airports:
              schedule_url=f"{schedule_url}?dep_iata={user_iata}&arr_iata={item['iata_code']}&api_key={self.api_key}"
              resp=requests.get(schedule_url)
              info=resp.json()
              if response in info:
                if len(info['response'])>0:
                    if len(Flight.objects.filter(event_id=id))<1: 
                        Flight.objects.create(event_name=the_event.event_name,event_id=id,flights_arriving=info['response'],flights_departing=[])
                        break
                    else:
                        flights_dep=get_object_or_404(Flight, event_id=id)
                        old_flights_departing=flights_dep['flights_departing']
                        Flight.objects.filter(event_id=id).delete()
                        Flight.objects.create(event_name=the_event.event_name,event_id=id,flights_arriving=info['response'],flights_departing=old_flights_departing)
                        break 
              
            # store data for departing mode
            # Store data in the model arriving part
            sorted_airports = sorted(data, key=lambda x: x["distance"])
            user_iata=iata_code
            schedule_url="https://airlabs.co/api/v9/schedules"
            for item in sorted_airports:
              schedule_url=f"{schedule_url}?dep_iata={item['iata_code']}&arr_iata={user_iata}&api_key={self.api_key}"
              respo=requests.get(schedule_url)
              info=respo.json()
              if response in info:
                if len(info['response'])>0:
                    if len(Flight.objects.filter(event_id=id))<1: 
                        Flight.objects.create(event_name=the_event.event_name,event_id=id,flights_departing=info['response'])
                        break
                    else:
                        flights_arr=get_object_or_404(Flight, event_id=id)
                        old_flights_arriv=flights_arr['flights_arriving']
                        Flight.objects.filter(event_id=id).delete()
                        Flight.objects.create(event_name=the_event.event_name,event_id=id,flights_arriving=old_flights_arriv,flights_departing=info['response'])
                        break
            # Retrieve filtered object
            queryset = Flight.objects.get(event_id=id)

            # Serialize the queryset
            serializer = FlightSerializer(queryset)

            # Return serialized data
            return Response(serializer.data)
        else:
            queryset = Flight.objects.get(event_id=id)
            serializer = FlightSerializer(queryset)
            return Response(serializer.data)

def HomeView(request):
    return HttpResponse("Welcome to the Reading List RESTful API!")
