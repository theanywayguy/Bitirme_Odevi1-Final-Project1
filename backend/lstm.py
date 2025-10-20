# Bu dosya, LSTM modelini kullanarak koordinatların tahmin edilmesi için bir sınıf içerir.

from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class LSTMPredictor:
    def __init__(self, model_path):
        self.model = load_model(model_path)

    def predict_trajectory(self, coords_list, seq_length):
        if len(coords_list) < seq_length:
            return []
        coords_scaled = np.array(coords_list)
        scaler = MinMaxScaler()
        coords_scaled = scaler.fit_transform(coords_scaled)
        predicted_points_scaled = []
        for i in range(len(coords_scaled) - seq_length):
            seq = coords_scaled[i:i + seq_length].reshape(1, seq_length, 2)
            pred = self.model.predict(seq, verbose=0)
            predicted_points_scaled.append(pred[0])
        predicted_points_scaled = np.array(predicted_points_scaled)
        predicted_points = scaler.inverse_transform(predicted_points_scaled)
        return predicted_points