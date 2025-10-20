# Bu dosya, videodan nesne tespiti yapmak için fonksiyonlar içerir.

import cv2
from backend.yolo import YoloDetector

def detect_objects(video_path, yolo_weights, conf_threshold=0.5):
    yolo = YoloDetector(yolo_weights)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    coords, detmap = [], {}
    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        xyxy, conf = yolo.detect(frame, conf_threshold)
        if xyxy is not None:
            x1, y1, x2, y2 = map(int, xyxy)
            x_c = (x1 + x2) / 2 / fw
            y_c = (y1 + y2) / 2 / fh
            y_flip = 1 - y_c
            coords.append([x_c, y_flip])
            detmap[frame_idx] = {
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "x_norm": x_c, "y_norm": y_c, "conf": conf
            }
        frame_idx += 1
    cap.release()
    return coords, detmap, fps, (fw, fh), total
