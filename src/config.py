"""
配置文件：包含项目的全局配置参数
"""

import os

# 路径配置 - 相对于项目根目录
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(_PROJECT_ROOT, "input")
OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "output")

# MediaPipe 配置
MEDIAPIPE_CONFIG = {
    'static_image_mode': False,
    'model_complexity': 2,  # 0, 1, 或 2 (2为最高精度)
    'smooth_landmarks': True,
    'enable_segmentation': False,
    'smooth_segmentation': True,
    'min_detection_confidence': 0.5,
    'min_tracking_confidence': 0.5
}

# 可视化配置
VISUALIZATION_CONFIG = {
    # 骨架线条颜色 (BGR格式)
    'skeleton_color': (0, 255, 0),  # 绿色
    'skeleton_thickness': 2,
    
    # 关键点颜色
    'landmark_color': (0, 0, 255),  # 红色
    'landmark_radius': 5,
    
    # 文字标注
    'text_color': (255, 255, 255),  # 白色
    'text_font': 0,  # cv2.FONT_HERSHEY_SIMPLEX
    'text_scale': 0.5,
    'text_thickness': 1,
    
    # 角度标注
    'angle_color': (255, 255, 0),  # 青色
    'angle_arc_radius': 30,
    
    # 背景透明度
    'info_box_alpha': 0.7
}

# 需要计算和显示的关节角度
ANGLES_TO_DISPLAY = [
    {
        'name': '左肘角度',
        'points': ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST'],
        'position': 'LEFT_ELBOW'
    },
    {
        'name': '右肘角度',
        'points': ['RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_WRIST'],
        'position': 'RIGHT_ELBOW'
    },
    {
        'name': '左膝角度',
        'points': ['LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE'],
        'position': 'LEFT_KNEE'
    },
    {
        'name': '右膝角度',
        'points': ['RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE'],
        'position': 'RIGHT_KNEE'
    },
    {
        'name': '左肩角度',
        'points': ['LEFT_ELBOW', 'LEFT_SHOULDER', 'LEFT_HIP'],
        'position': 'LEFT_SHOULDER'
    },
    {
        'name': '右肩角度',
        'points': ['RIGHT_ELBOW', 'RIGHT_SHOULDER', 'RIGHT_HIP'],
        'position': 'RIGHT_SHOULDER'
    }
]

# MediaPipe 骨架连接定义
POSE_CONNECTIONS = [
    # 躯干
    ('LEFT_SHOULDER', 'RIGHT_SHOULDER'),
    ('LEFT_SHOULDER', 'LEFT_HIP'),
    ('RIGHT_SHOULDER', 'RIGHT_HIP'),
    ('LEFT_HIP', 'RIGHT_HIP'),
    
    # 左臂
    ('LEFT_SHOULDER', 'LEFT_ELBOW'),
    ('LEFT_ELBOW', 'LEFT_WRIST'),
    ('LEFT_WRIST', 'LEFT_PINKY'),
    ('LEFT_WRIST', 'LEFT_INDEX'),
    ('LEFT_WRIST', 'LEFT_THUMB'),
    
    # 右臂
    ('RIGHT_SHOULDER', 'RIGHT_ELBOW'),
    ('RIGHT_ELBOW', 'RIGHT_WRIST'),
    ('RIGHT_WRIST', 'RIGHT_PINKY'),
    ('RIGHT_WRIST', 'RIGHT_INDEX'),
    ('RIGHT_WRIST', 'RIGHT_THUMB'),
    
    # 左腿
    ('LEFT_HIP', 'LEFT_KNEE'),
    ('LEFT_KNEE', 'LEFT_ANKLE'),
    ('LEFT_ANKLE', 'LEFT_HEEL'),
    ('LEFT_ANKLE', 'LEFT_FOOT_INDEX'),
    
    # 右腿
    ('RIGHT_HIP', 'RIGHT_KNEE'),
    ('RIGHT_KNEE', 'RIGHT_ANKLE'),
    ('RIGHT_ANKLE', 'RIGHT_HEEL'),
    ('RIGHT_ANKLE', 'RIGHT_FOOT_INDEX'),
    
    # 脸部
    ('NOSE', 'LEFT_EYE'),
    ('LEFT_EYE', 'LEFT_EAR'),
    ('NOSE', 'RIGHT_EYE'),
    ('RIGHT_EYE', 'RIGHT_EAR'),
    ('MOUTH_LEFT', 'MOUTH_RIGHT'),
]

# 视频处理配置
VIDEO_CONFIG = {
    'output_fps': None,  # None表示使用输入视频的fps
    'output_codec': 'mp4v',  # 输出视频编码器
    'show_progress': True
}

