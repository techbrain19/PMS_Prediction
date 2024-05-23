from django import forms
from .models import FuelPrediction

class FuelPredictionForm(forms.ModelForm):
    class Meta:
        model = FuelPrediction
        fields = ['date']