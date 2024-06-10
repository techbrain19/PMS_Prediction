import os
from sklearn.preprocessing import StandardScaler
from keras.models import load_model
from django.db import models

class FuelPrediction(models.Model):
    date = models.DateField()
    price = models.FloatField()
    fuel_price_in_naira = models.FloatField(null=True, blank=True)
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    model_path = os.path.join(os.path.dirname(__file__), 'fuel_price_prediction_model.h5')
    try:
        model = load_model(model_path)
    except OSError:
        print("Error: Fuel price prediction model not found.")
        model = None

    scaler = StandardScaler()

    def predict_fuel_price(self):
        X = np.array([[self.date.year, self.date.month, self.date.day]])
        X = self.scaler.fit_transform(X)

        if self.model is not None:
            self.predicted_price = self.model.predict(X)[0][0]
        else:
            self.predicted_price = 0.0

        return self.predicted_price