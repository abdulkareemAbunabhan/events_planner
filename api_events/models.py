from django.db import models

# Create your models here.
class Event (models.Model):
    event_name = models.CharField(max_length=64)
    event_id = models.CharField(max_length=64)
    event_date = models.CharField(max_length=64)
    event_lat= models.FloatField()
    event_lon= models.FloatField()
    desc = models.TextField()
    event_country=models.CharField(max_length=32,default="None")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.event_name

class Weather(models.Model):
       event_name = models.CharField(max_length=64) 
       event_id = models.CharField(max_length=64)
       event_Temperature = models.FloatField()
       event_Humidity = models.FloatField()
       created_at = models.DateTimeField(auto_now_add=True)
       def __str__(self):
        return self.event_name 

class Flight(models.Model):
       event_name = models.CharField(max_length=64) 
       event_id = models.CharField(max_length=64)
       flights_arriving = models.JSONField()
       flights_departing = models.JSONField()
       created_at = models.DateTimeField(auto_now_add=True)
       def __str__(self):
        return self.event_name