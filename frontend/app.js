function updateProgressBar(bar, value) {
  bar.style.width = value + "%";
}

function displayCSV(csvText) {
  const lines = csvText.trim().split("\n");
  const headers = lines[0].split(",");
  const maxRows = Math.min(lines.length - 1, 10);
  let html = "<table class='min-w-full border-collapse border border-gray-300'>";
  html += "<thead><tr>" + headers.map(h => `<th class='border border-gray-300 px-2 py-1 bg-gray-200'>${h}</th>`).join("") + "</tr></thead><tbody>";
  for (let i = 1; i <= maxRows; i++) {
    const cells = lines[i].split(",");
    html += "<tr>" + cells.map(c => `<td class='border border-gray-300 px-2 py-1'>${c}</td>`).join("") + "</tr>";
  }
  html += "</tbody></table>";
  if (lines.length - 1 > 10) html += `<p class='text-sm text-gray-500 mt-1'>Toplam ${lines.length - 1} satır var. Yalnızca ilk 10 gösteriliyor.</p>`;
  return html;
}

function displayMetrics(metrics) {
  return `
    <div class="metric-card">
      <h3>Toplam MSE</h3>
      <p>${metrics.mse_total.toFixed(4)}</p>
    </div>
    <div class="metric-card">
      <h3>Toplam MAE</h3>
      <p>${metrics.mae_total.toFixed(4)}</p>
    </div>
    <div class="metric-card">
      <h3>MAE (X)</h3>
      <p>${metrics.mae_x.toFixed(4)}</p>
    </div>
    <div class="metric-card">
      <h3>MAE (Y)</h3>
      <p>${metrics.mae_y.toFixed(4)}</p>
    </div>
    <div class="metric-card">
      <h3>Toplam Doğruluk</h3>
      <p>${metrics.accuracy_total.toFixed(2)}%</p>
    </div>
    <div class="metric-card">
      <h3>X Doğruluğu</h3>
      <p>${metrics.accuracy_x.toFixed(2)}%</p>
    </div>
    <div class="metric-card">
      <h3>Y Doğruluğu</h3>
      <p>${metrics.accuracy_y.toFixed(2)}%</p>
    </div>
  `;
}

function disableButton(button, disable = true) {
  if (disable) {
    button.disabled = true;
    button.classList.add('opacity-50', 'cursor-not-allowed');
  } else {
    button.disabled = false;
    button.classList.remove('opacity-50', 'cursor-not-allowed');
  }
}

async function uploadFile(url, file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(url, { method: "POST", body: formData });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// Görsel yükleme
document.getElementById("uploadImageBtn").addEventListener("click", async () => {
  const fileInput = document.getElementById("imageInput");
  const progressBar = document.getElementById("imageProgress");
  const resultDiv = document.getElementById("imageResult");
  const imgEl = document.getElementById("processedImage");
  const dlLink = document.getElementById("downloadImage");
  const uploadBtn = document.getElementById("uploadImageBtn");

  if (!fileInput.files.length) return alert("Bir dosya seçiniz.");
  const file = fileInput.files[0];
  const ext = file.name.split('.').pop().toLowerCase();
  if (!["jpg", "jpeg", "png"].includes(ext)) return alert("Sadece .jpg, .jpeg, .png desteklenir.");

  disableButton(uploadBtn, true);
  updateProgressBar(progressBar, 10);
  
  try {
    const data = await uploadFile("/upload_image", file);
    updateProgressBar(progressBar, 70);
    const imageUrl = `/result/${data.filename}`;
    imgEl.src = imageUrl;
    dlLink.href = imageUrl;
    resultDiv.classList.remove("hidden");
    updateProgressBar(progressBar, 100);
  } catch (err) {
    alert("Hata: " + err.message);
    updateProgressBar(progressBar, 0);
  } finally {
    disableButton(uploadBtn, false);
  }
});

// Video yükleme
document.getElementById("uploadVideoBtn").addEventListener("click", async () => {
  const fileInput = document.getElementById("videoInput");
  const progressBar = document.getElementById("videoProgress");
  const stepContainer = document.getElementById("videoSteps");
  const resultDiv = document.getElementById("videoResult");
  const videoEl = document.getElementById("processedVideo");
  const metricsDiv = document.getElementById("metricsResult");
  const trajImg = document.getElementById("trajGraph");
  const xyImg = document.getElementById("xyGraph");
  const csvDiv = document.getElementById("csvResult");

  const dlVideo = document.getElementById("downloadVideo");
  const dlCSV = document.getElementById("downloadCSV");
  const dlTraj = document.getElementById("downloadTraj");
  const dlXY = document.getElementById("downloadXY");
  const uploadBtn = document.getElementById("uploadVideoBtn");

  if (!fileInput.files.length) return alert("Bir dosya seçiniz.");
  const file = fileInput.files[0];
  const ext = file.name.split('.').pop().toLowerCase();
  if (ext !== "mp4") return alert("Sadece .mp4 desteklenir.");

  disableButton(uploadBtn, true);
  stepContainer.innerHTML = `
    <div class="step-item active">
      <div class="step-icon"></div>
      <div class="step-text">Yükleniyor...</div>
    </div>
  `;
  updateProgressBar(progressBar, 10);

  let data;
  try {
    data = await uploadFile("/upload_video", file);
  } catch (err) {
    alert("Yükleme hatası: " + err.message);
    stepContainer.innerHTML = `
      <div class="step-item error">
        <div class="step-icon"></div>
        <div class="step-text">Hata oluştu</div>
      </div>
    `;
    updateProgressBar(progressBar, 0);
    disableButton(uploadBtn, false);
    return;
  }

  const ws = new WebSocket(`ws://${window.location.host}/ws/progress/${data.task_id}`);
  let currentStep = null;
  
  ws.onmessage = async (event) => {
    const msg = JSON.parse(event.data);
    
    if (msg.step && msg.step !== currentStep) {
      updateStepProgress(msg.step);
      currentStep = msg.step;
    }

    if (msg.step === "Complete") {
      ws.close();
      
      const videoUrl = `/result/${data.video_filename}`;
      const csvUrl = `/result/${data.csv_filename}`;
      const trajUrl = `/result/${data.traj_graph_filename}`;
      const xyUrl = `/result/${data.xy_graph_filename}`;

      videoEl.src = videoUrl;
      trajImg.src = trajUrl;
      xyImg.src = xyUrl;
      dlVideo.href = videoUrl;
      dlTraj.href = trajUrl;
      dlXY.href = xyUrl;

      const csvRes = await fetch(csvUrl);
      const csvText = await csvRes.text();
      csvDiv.innerHTML = displayCSV(csvText);
      dlCSV.href = csvUrl;

      if (msg.metrics) {
        metricsDiv.innerHTML = displayMetrics(msg.metrics);
        metricsDiv.classList.remove("hidden");
      }

      resultDiv.classList.remove("hidden");
      updateProgressBar(progressBar, 100);
      disableButton(uploadBtn, false);
    }
  };

  function updateStepProgress(step) {
    const stepMessages = {
      "YOLO Detection": "YOLO ile nesne algılanıyor...",
      "CSV Generation": "Koordinat verileri CSV formatına dönüştürülüyor...",
      "LSTM Prediction": "LSTM modeli ile hareket tahmini yapılıyor...",
      "Video Annotation": "Videoya açıklamalar ekleniyor...",
      "Graph Generation": "Grafikler oluşturuluyor...",
      "Complete": "İşlem tamamlandı"
    };

    const message = stepMessages[step] || step;
    
    const currentStepElement = stepContainer.querySelector('.step-item.active');
    if (currentStepElement) {
      currentStepElement.classList.remove('active');
      currentStepElement.classList.add('completed');
    }

    const newStepHtml = `
      <div class="step-item active">
        <div class="step-icon"></div>
        <div class="step-text">${message}</div>
      </div>
    `;
    stepContainer.insertAdjacentHTML('beforeend', newStepHtml);

    const progressMap = {
      "YOLO Detection": 25,
      "CSV Generation": 45,
      "LSTM Prediction": 65,
      "Video Annotation": 80,
      "Graph Generation": 95,
      "Complete": 100
    };
    if (progressMap[step]) updateProgressBar(progressBar, progressMap[step]);
  }

  ws.onerror = () => {
    alert("WebSocket bağlantısı başarısız oldu.");
    stepContainer.innerHTML = `
      <div class="step-item error">
        <div class="step-icon"></div>
        <div class="step-text">Bağlantı hatası</div>
      </div>
    `;
    updateProgressBar(progressBar, 0);
    disableButton(uploadBtn, false);
  };
});
