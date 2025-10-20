#Bu dosya, FastAPI kullanarak yüklenen görüntülerde nesne tespiti yapmak için bir API uç noktası sağlar.

from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid, os, cv2, numpy as np
from backend.yolo import YoloDetector
from backend.core.config import YOLO_WEIGHTS, OUTPUT_DIR

router = APIRouter()

@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    ext = file.filename.split('.')[-1].lower()
    if ext not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Unsupported image type")

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    yolo = YoloDetector(YOLO_WEIGHTS)
    xyxy, conf = yolo.detect(img)
    if xyxy is None:
        raise HTTPException(status_code=400, detail="No object detected")

    x1, y1, x2, y2 = map(int, xyxy)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(img, f"Top G:{conf:.2f}", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    out_name = f"{uuid.uuid4()}.{ext}"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    if not cv2.imwrite(out_path, img):
        raise HTTPException(status_code=500, detail="Failed to save image")

    return {"filename": out_name, "type": "image"}
