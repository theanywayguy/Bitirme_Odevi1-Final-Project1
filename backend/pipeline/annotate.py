#Bu dosya, videolara tespit kutuları ve tahmin edilen noktalar eklemek için fonksiyonlar içerir.
import cv2

def annotate_video(video_path, detmap, predicted_points, output_video_path,
                   fps, frame_dims, total_frames, seq_length):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_dims)
    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if idx in detmap:
            d = detmap[idx]
            cv2.rectangle(frame, (d["x1"], d["y1"]), (d["x2"], d["y2"]), (0, 255, 0), 2)
            cv2.putText(frame, f"Top ({d['x_norm']:.2f},{d['y_norm']:.2f}) G:{d['conf']:.2f}",
                        (d["x1"], d["y1"] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        pred_i = idx - seq_length
        if 0 <= pred_i < len(predicted_points):
            x_p, y_f = predicted_points[pred_i]
            x_pix = int(x_p * frame_dims[0])
            y_pix = int((1 - y_f) * frame_dims[1])
            cv2.circle(frame, (x_pix, y_pix), 8, (0, 165, 255), -1)
        out.write(frame)
        idx += 1
    cap.release()
    out.release()
