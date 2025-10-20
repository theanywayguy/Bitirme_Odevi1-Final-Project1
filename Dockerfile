# Python 3.13 taban imajı
FROM python:3.13-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Önce yalnızca requirements.txt'yi kopyala, önbellek için
COPY requirements.txt .

# Önce Torch CPU'yu yükle
RUN pip install --no-cache-dir torch==2.9.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Sonra geri kalan paketleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# FastAPI varsayılan portunu aç
EXPOSE 8000

# FastAPI uygulamasını uvicorn ile çalıştır
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
