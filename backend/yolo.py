# Bu dosya, YOLO modelini kullanarak nesne tespiti yapmak için bir sınıf içerir.

from ultralytics import YOLO

class YoloDetector:
    def __init__(self, weights_path):
        self.model = YOLO(weights_path)

    def detect(self, frame, conf_threshold=0.5):
        results = self.model.predict(frame, verbose=False, conf=conf_threshold)
        for result in results:
            boxes = result.boxes
            if len(boxes) > 0:
                box = boxes[0]
                xyxy = box.xyxy[0].cpu().numpy()  # Use cpu().numpy() for compatibility
                conf = float(box.conf[0])
                return xyxy, conf
        return None, None