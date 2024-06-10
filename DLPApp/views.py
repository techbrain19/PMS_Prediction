from django.shortcuts import render, redirect
from .forms import FuelPredictionForm
from .models import FuelPrediction

def index(request):
    if request.method == 'POST':
        form = FuelPredictionForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            fuel_price_in_naira = form.cleaned_data['price']
            fuel_prediction = FuelPrediction(date=date, fuel_price_in_naira=fuel_price_in_naira)
            predicted_price = fuel_prediction.predict_fuel_price()
            fuel_prediction.price = 0.0
            fuel_prediction.predicted_price = predicted_price
            fuel_prediction.save()

            return redirect('result', pk=fuel_prediction.id)
    else:
        form = FuelPredictionForm()
    return render(request, 'DLPApp/index.html',  {'form': form})


def result(request, pk):
    fuel_prediction = FuelPrediction.objects.get(pk=pk)
    return render(request, 'DLPApp/result.html', {'fuel_prediction': fuel_prediction})