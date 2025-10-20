# Bu dosya temel dizinleri ve model yollarını tanımlar, çıktı klasörünü oluşturur.
# YOLO ve LSTM modellerinin dosya yollarını merkezi olarak saklamak için kullanılır.
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

YOLO_WEIGHTS = os.path.join(BASE_DIR, "models", "best.pt")
LSTM_MODEL = os.path.join(BASE_DIR, "models", "trained_lstm_ball.keras")
