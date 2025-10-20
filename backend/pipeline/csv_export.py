# Bu dosya, koordinat verilerini CSV dosyasına aktarmak için fonksiyonlar içerir.

import pandas as pd

def export_csv(coords_list, csv_path):
    df = pd.DataFrame(coords_list, columns=["x_norm", "y_norm_flipped"])
    df.to_csv(csv_path, index=False)
