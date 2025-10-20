# Bu dosya, gerçek ve tahmin edilen koordinatları kullanarak grafikler oluşturmak ve performans metriklerini hesaplamak için fonksiyonlar içerir.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

def generate_graphs_and_metrics(coords_list, predicted_points, seq_length, traj_path, xy_path):
    if len(predicted_points) == 0:
        return {}

    y_true = np.array(coords_list[seq_length:len(predicted_points)+seq_length])
    y_pred = np.array(predicted_points)

    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    mae_x = mean_absolute_error(y_true[:,0], y_pred[:,0])
    mae_y = mean_absolute_error(y_true[:,1], y_pred[:,1])

    metrics = {
        "mse_total": mse,
        "mae_total": mae,
        "mae_x": mae_x,
        "mae_y": mae_y,
        "accuracy_total": (1 - mae) * 100,
        "accuracy_x": (1 - mae_x) * 100,
        "accuracy_y": (1 - mae_y) * 100
    }

    plt.figure(figsize=(10,6))
    plt.plot(y_true[:,0], y_true[:,1], label="Gerçek")
    plt.plot(y_pred[:,0], y_pred[:,1], label="Tahmin")
    plt.gca().invert_yaxis()
    plt.legend(); plt.grid(True)
    plt.tight_layout(); plt.savefig(traj_path); plt.close()

    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.plot(y_true[:,0], label="Gerçek X")
    plt.plot(y_pred[:,0], label="Tahmin X")
    plt.legend(); plt.grid(True)
    plt.subplot(1,2,2)
    plt.plot(y_true[:,1], label="Gerçek Y")
    plt.plot(y_pred[:,1], label="Tahmin Y")
    plt.legend(); plt.grid(True)
    plt.tight_layout(); plt.savefig(xy_path); plt.close()

    return metrics
