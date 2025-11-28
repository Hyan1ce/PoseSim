import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(_PROJECT_ROOT, "input")
OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "output")

MEDIAPIPE_CONFIG = {
    'static_image_mode': False,
    'model_complexity': 2,
    'smooth_landmarks': True,
    'enable_segmentation': False,
    'smooth_segmentation': True,
    'min_detection_confidence': 0.5,
    'min_tracking_confidence': 0.5
}

VISUALIZATION_CONFIG = {
    'skeleton_color': (0, 255, 0),
    'skeleton_thickness': 2,
    'landmark_color': (0, 0, 255),
    'landmark_radius': 5,
    'text_color': (255, 255, 255),
    'text_font': 0,
    'text_scale': 0.5,
    'text_thickness': 1,
    'angle_color': (255, 255, 0),
    'angle_arc_radius': 30,
    'info_box_alpha': 0.7
}
ANGLES_TO_DISPLAY = [
    {'name': '左肘角度', 'points': ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST'], 'position': 'LEFT_ELBOW'},
    {'name': '右肘角度', 'points': ['RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_WRIST'], 'position': 'RIGHT_ELBOW'},
    {'name': '左膝角度', 'points': ['LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE'], 'position': 'LEFT_KNEE'},
    {'name': '右膝角度', 'points': ['RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE'], 'position': 'RIGHT_KNEE'},
    {'name': '左肩角度', 'points': ['LEFT_ELBOW', 'LEFT_SHOULDER', 'LEFT_HIP'], 'position': 'LEFT_SHOULDER'},
    {'name': '右肩角度', 'points': ['RIGHT_ELBOW', 'RIGHT_SHOULDER', 'RIGHT_HIP'], 'position': 'RIGHT_SHOULDER'}
]

POSE_CONNECTIONS = [
    ('LEFT_SHOULDER', 'RIGHT_SHOULDER'),
    ('LEFT_SHOULDER', 'LEFT_HIP'),
    ('RIGHT_SHOULDER', 'RIGHT_HIP'),
    ('LEFT_HIP', 'RIGHT_HIP'),
    ('LEFT_SHOULDER', 'LEFT_ELBOW'),
    ('LEFT_ELBOW', 'LEFT_WRIST'),
    ('LEFT_WRIST', 'LEFT_PINKY'),
    ('LEFT_WRIST', 'LEFT_INDEX'),
    ('LEFT_WRIST', 'LEFT_THUMB'),
    ('RIGHT_SHOULDER', 'RIGHT_ELBOW'),
    ('RIGHT_ELBOW', 'RIGHT_WRIST'),
    ('RIGHT_WRIST', 'RIGHT_PINKY'),
    ('RIGHT_WRIST', 'RIGHT_INDEX'),
    ('RIGHT_WRIST', 'RIGHT_THUMB'),
    ('LEFT_HIP', 'LEFT_KNEE'),
    ('LEFT_KNEE', 'LEFT_ANKLE'),
    ('LEFT_ANKLE', 'LEFT_HEEL'),
    ('LEFT_ANKLE', 'LEFT_FOOT_INDEX'),
    ('RIGHT_HIP', 'RIGHT_KNEE'),
    ('RIGHT_KNEE', 'RIGHT_ANKLE'),
    ('RIGHT_ANKLE', 'RIGHT_HEEL'),
    ('RIGHT_ANKLE', 'RIGHT_FOOT_INDEX'),
    ('NOSE', 'LEFT_EYE'),
    ('LEFT_EYE', 'LEFT_EAR'),
    ('NOSE', 'RIGHT_EYE'),
    ('RIGHT_EYE', 'RIGHT_EAR'),
    ('MOUTH_LEFT', 'MOUTH_RIGHT'),
]

VIDEO_CONFIG = {
    'output_fps': None,
    'output_codec': 'mp4v',
    'show_progress': True
}

