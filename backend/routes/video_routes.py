from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from backend.pipeline.video_utils import process_video
from backend.core.config import YOLO_WEIGHTS, LSTM_MODEL, OUTPUT_DIR
from backend.core.progress import update_progress
import os, uuid, cv2

router = APIRouter()

async def process_video_task(task_id, temp_path, video_name, csv_name, traj_name, xy_name):
    try:
        for update in process_video(temp_path, YOLO_WEIGHTS, LSTM_MODEL,
                                    os.path.join(OUTPUT_DIR, video_name),
                                    os.path.join(OUTPUT_DIR, csv_name),
                                    os.path.join(OUTPUT_DIR, traj_name),
                                    os.path.join(OUTPUT_DIR, xy_name)):
            update_progress(task_id, update)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/upload_video")
async def upload_video(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    ext = file.filename.split('.')[-1].lower()
    if ext not in ["mp4", "avi"]:
        raise HTTPException(status_code=400, detail="Unsupported video type")

    temp_name = f"{uuid.uuid4()}.{ext}"
    temp_path = os.path.join(OUTPUT_DIR, temp_name)
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    cap = cv2.VideoCapture(temp_path)
    if not cap.isOpened():
        os.remove(temp_path)
        raise HTTPException(status_code=400, detail="Invalid video")
    frame_count, fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps if fps > 0 else 0
    cap.release()
    if duration > 60:
        os.remove(temp_path)
        raise HTTPException(status_code=400, detail="Video too long")

    task_id = str(uuid.uuid4())
    video_name = f"{uuid.uuid4()}.webm"
    csv_name = f"{uuid.uuid4()}.csv"
    traj_name = f"{uuid.uuid4()}_traj.png"
    xy_name = f"{uuid.uuid4()}_xy.png"

    background_tasks.add_task(process_video_task, task_id, temp_path,
                              video_name, csv_name, traj_name, xy_name)

    return {
        "task_id": task_id,
        "video_filename": video_name,
        "csv_filename": csv_name,
        "traj_graph_filename": traj_name,
        "xy_graph_filename": xy_name,
        "type": "video"
    }

@router.get("/result/{filename}")
async def get_result(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    mt = None
    if path.endswith(".webm"):
        mt = "video/webm"
    elif path.endswith(".csv"):
        mt = "text/csv"
    elif path.endswith(".png"):
        mt = "image/png"
    return FileResponse(path, media_type=mt)
