# Bu dosya, LSTM modelini kullanarak koordinatların tahmin edilmesi için fonksiyonlar içerir.

from backend.lstm import LSTMPredictor

def run_lstm_prediction(coords_list, model_path, seq_length):
    lstm = LSTMPredictor(model_path)
    return lstm.predict_trajectory(coords_list, seq_length)
