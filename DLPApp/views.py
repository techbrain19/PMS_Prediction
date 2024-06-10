from django.shortcuts import render, redirect
from .forms import FuelPredictionForm
from .models import FuelPrediction

def index(request):
    if request.method == 'POST':
        form = FuelPredictionForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            fuel_prediction = FuelPrediction(date=date)
            try:
                predicted_price = fuel_prediction.predict_fuel_price()
                if predicted_price is not None:
                    fuel_prediction.predicted_price = predicted_price
                    fuel_prediction.save()
                    return redirect('result', pk=fuel_prediction.id)
                else:
                    error_message = "Error occurred while predicting fuel price."
                    return render(request, 'DLPApp/index.html', {'form': form, 'error_message': error_message})
            except (FileNotFoundError, ValueError, IndexError) as e:
                error_message = f"Error occurred: {e}"
                return render(request, 'DLPApp/index.html', {'form': form, 'error_message': error_message})
    else:
        form = FuelPredictionForm()
    return render(request, 'DLPApp/index.html', {'form': form})

def result(request, pk):
    fuel_prediction = FuelPrediction.objects.get(pk=pk)
    return render(request, 'DLPApp/result.html', {'fuel_prediction': fuel_prediction})