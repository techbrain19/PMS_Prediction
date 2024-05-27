from django.shortcuts import render, redirect
from .forms import FuelPredictionForm
from .models import FuelPrediction

def index(request):
    if request.method == 'POST':
        form = FuelPredictionForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            fuel_price_in_naira = form.cleaned_data['fuel_price_in_naira']

            # Create a new FuelPrediction instance and make the prediction
            fuel_prediction = FuelPrediction(date=date, fuel_price_in_naira=fuel_price_in_naira)
            predicted_price = fuel_prediction.predict_fuel_price()

            # Save the FuelPrediction instance
            fuel_prediction.price = 0.0  # Actual price not provided, set to 0
            fuel_prediction.predicted_price = predicted_price
            fuel_prediction.save()

            return redirect('result', pk=fuel_prediction.id)
    else:
        form = FuelPredictionForm()
    return render(request, 'DLPApp/index.html',  {'form': form})

import numpy as np
import os
from django.shortcuts import render, redirect
from .forms import FuelPredictionForm
from .models import FuelPrediction
from sklearn.preprocessing import StandardScaler
from keras.models import load_model

def index(request):
    if request.method == 'POST':
        form = FuelPredictionForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']

            # Load the pre-trained Keras model
            model_path = os.path.join(os.path.dirname(__file__), 'fuel_price_prediction_model.h5')
            model = load_model(model_path)

            # Prepare the input data
            X = np.array([[date.year, date.month, date.day]])
            X = StandardScaler().fit_transform(X)

            # Make the prediction
            predicted_price = model.predict(X)[0][0]

            # Save the prediction to the database
            fuel_prediction = FuelPrediction(
                date=date,
                price=0.0,  # Actual price not provided, set to 0
                predicted_price = predicted_price
            )
            fuel_prediction.save()

            return redirect('result', pk=fuel_prediction.id)
    else:
        form = FuelPredictionForm()
    return render(request, 'DLPApp/index.html',  {'form': form})

def result(request, pk):
    fuel_prediction = FuelPrediction.objects.get(pk=pk)
    return render(request, 'DLPApp/result.html', {'fuel_prediction': fuel_prediction})