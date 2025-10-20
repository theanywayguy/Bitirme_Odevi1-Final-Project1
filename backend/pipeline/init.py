from .detect import detect_objects
from .csv_export import export_csv
from .predict import run_lstm_prediction
from .annotate import annotate_video
from .graphs import generate_graphs_and_metrics

def process_video(video_path, yolo_weights, lstm_model_path,
                  output_video_path, csv_path, traj_path, xy_path,
                  seq_length=10, conf_threshold=0.5):
    yield {"step": "YOLO Detection", "progress": 0}
    coords_list, detection_map, fps, frame_dims, total_frames = detect_objects(video_path, yolo_weights, conf_threshold)
    yield {"step": "YOLO Detection", "progress": 20}

    yield {"step": "CSV Generation", "progress": 20}
    export_csv(coords_list, csv_path)
    yield {"step": "CSV Generation", "progress": 40}

    yield {"step": "LSTM Prediction", "progress": 40}
    predicted_points = run_lstm_prediction(coords_list, lstm_model_path, seq_length)
    yield {"step": "LSTM Prediction", "progress": 60}

    yield {"step": "Video Annotation", "progress": 60}
    annotate_video(video_path, detection_map, predicted_points, output_video_path, fps, frame_dims, total_frames, seq_length)
    yield {"step": "Video Annotation", "progress": 80}

    yield {"step": "Graph Generation", "progress": 80}
    metrics = generate_graphs_and_metrics(coords_list, predicted_points, seq_length, traj_path, xy_path)
    yield {"step": "Graph Generation", "progress": 100, "metrics": metrics}
