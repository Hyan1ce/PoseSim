import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Dict, List, Tuple
from config import MEDIAPIPE_CONFIG


class PoseEstimator:
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or MEDIAPIPE_CONFIG
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(**self.config)
        
        self.landmark_names = [landmark.name for landmark in self.mp_pose.PoseLandmark]
        self.landmark_dict = {name: idx for idx, name in enumerate(self.landmark_names)}
    
    def estimate(self, image: np.ndarray) -> Optional[object]:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.pose.process(image_rgb)
        image_rgb.flags.writeable = True
        return results
    
    def get_landmark_coords(self, results: object, landmark_name: str, 
                           image_shape: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        if not results.pose_landmarks:
            return None
        
        try:
            landmark_idx = self.landmark_dict[landmark_name]
            landmark = results.pose_landmarks.landmark[landmark_idx]
            
            h, w = image_shape
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            
            if landmark.visibility < 0.5:
                return None
                
            return (x, y)
        except (KeyError, IndexError):
            return None
    
    def get_all_landmarks(self, results: object, 
                         image_shape: Tuple[int, int]) -> Dict[str, Tuple[int, int]]:
        landmarks_dict = {}
        
        if not results.pose_landmarks:
            return landmarks_dict
        
        h, w = image_shape
        for name in self.landmark_names:
            coords = self.get_landmark_coords(results, name, image_shape)
            if coords:
                landmarks_dict[name] = coords
        
        return landmarks_dict
    
    def calculate_angle(self, point1: Tuple[int, int], 
                       point2: Tuple[int, int], 
                       point3: Tuple[int, int]) -> float:
        p1 = np.array(point1)
        p2 = np.array(point2)
        p3 = np.array(point3)
        
        vector1 = p1 - p2
        vector2 = p3 - p2
        
        cos_angle = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = np.arccos(cos_angle)
        
        return np.degrees(angle)
    
    def calculate_distance(self, point1: Tuple[int, int], 
                          point2: Tuple[int, int]) -> float:
        p1 = np.array(point1)
        p2 = np.array(point2)
        return np.linalg.norm(p1 - p2)
    
    def __del__(self):
        self.pose.close()

