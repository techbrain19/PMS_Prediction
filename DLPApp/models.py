import numpy as np
import pandas as pd
from django.db import models
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
import xgboost as xgb

class FuelPrediction(models.Model):
    date = models.DateField()
    fuel_price_in_naira = models.FloatField()
    price = models.FloatField(default=0.0)
    predicted_price = models.FloatField(default=0.0)

    def predict_fuel_price(self):
        try:
            pms_price = pd.read_csv('data/crude_oil_price.csv')
            geopolitacal_event = pd.read_csv('data/Pol_Data.csv')
            exchange_rate = pd.read_csv('data/USD_NGN_Historical_Data.csv')
            data = pd.concat([pms_price, geopolitacal_event, exchange_rate], ignore_index=True)
            data['date'] = pd.to_datetime(data['date'])
            X = data['date'].values.reshape(-1, 1)
            y = data['price']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            models = {
                'Linear Regression': LinearRegression(),
                'SVR': SVR(),
                'GBR': GradientBoostingRegressor(),
                'MLP': MLPRegressor(),
                'XGBoost': xgb.XGBRegressor()
            }
            best_r2 = -float('inf')
            best_model = None
            for name, model in models.items():
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                print(f"{name} - MSE: {mse:.2f}, MAE: {mae:.2f}, R-squared: {r2:.2f}")
                if r2 > best_r2:
                    best_model = model
                    best_r2 = r2

            date_input = np.array([[self.date.to_numpy()]]).reshape(-1, 1)
            if self.date <= data['date'].max():
                predicted_price = data[data['date'] == self.date]['price'].values[0]
            else:
                predicted_price = best_model.predict(date_input)[0]
            return predicted_price
        except (FileNotFoundError, ValueError, IndexError) as e:
            print(f"Error occurred: {e}")
            return None