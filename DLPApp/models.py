from django.db import models

class FuelPrediction(models.Model):
    date = models.DateField()
    fuel_type = models.CharField(max_length=50)
    price = models.FloatField()
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)