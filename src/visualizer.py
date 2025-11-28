import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
from config import VISUALIZATION_CONFIG, POSE_CONNECTIONS, ANGLES_TO_DISPLAY
from pose_estimator import PoseEstimator


class PoseVisualizer:
    
    def __init__(self, pose_estimator: PoseEstimator, config: Optional[Dict] = None):
        self.estimator = pose_estimator
        self.config = config or VISUALIZATION_CONFIG
    
    def draw_skeleton(self, image: np.ndarray, 
                     landmarks: Dict[str, Tuple[int, int]]) -> np.ndarray:
        output = image.copy()
        
        for connection in POSE_CONNECTIONS:
            point1_name, point2_name = connection
            
            if point1_name in landmarks and point2_name in landmarks:
                point1 = landmarks[point1_name]
                point2 = landmarks[point2_name]
                
                cv2.line(output, point1, point2,
                        self.config['skeleton_color'],
                        self.config['skeleton_thickness'])
        
        for point_name, coords in landmarks.items():
            cv2.circle(output, coords,
                      self.config['landmark_radius'],
                      self.config['landmark_color'],
                      -1)
        
        return output
    
    def draw_angle_arc(self, image: np.ndarray, center: Tuple[int, int],
                      angle: float, start_point: Tuple[int, int],
                      end_point: Tuple[int, int]) -> np.ndarray:
        start_vector = np.array(start_point) - np.array(center)
        end_vector = np.array(end_point) - np.array(center)
        
        start_angle = np.degrees(np.arctan2(start_vector[1], start_vector[0]))
        end_angle = np.degrees(np.arctan2(end_vector[1], end_vector[0]))
        
        radius = self.config['angle_arc_radius']
        cv2.ellipse(image, center, (radius, radius), 0,
                   start_angle, end_angle,
                   self.config['angle_color'], 2)
        
        return image
    
    def draw_angles(self, image: np.ndarray,
                   landmarks: Dict[str, Tuple[int, int]]) -> np.ndarray:
        output = image.copy()
        
        for angle_info in ANGLES_TO_DISPLAY:
            point_names = angle_info['points']
            
            if all(name in landmarks for name in point_names):
                point1 = landmarks[point_names[0]]
                point2 = landmarks[point_names[1]]
                point3 = landmarks[point_names[2]]
                
                angle = self.estimator.calculate_angle(point1, point2, point3)
                label_pos = landmarks[angle_info['position']]
                
                text = f"{angle:.1f}°"
                text_size = cv2.getTextSize(text, self.config['text_font'],
                                           self.config['text_scale'],
                                           self.config['text_thickness'])[0]
                
                text_x = label_pos[0] + 15
                text_y = label_pos[1] - 15
                
                overlay = output.copy()
                cv2.rectangle(overlay,
                            (text_x - 2, text_y - text_size[1] - 2),
                            (text_x + text_size[0] + 2, text_y + 2),
                            (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.6, output, 0.4, 0, output)
                
                cv2.putText(output, text,
                          (text_x, text_y),
                          self.config['text_font'],
                          self.config['text_scale'],
                          self.config['angle_color'],
                          self.config['text_thickness'])
        
        return output
    
    def draw_info_panel(self, image: np.ndarray, frame_num: int,
                       total_frames: int, fps: float) -> np.ndarray:
        output = image.copy()
        h, w = output.shape[:2]
        
        overlay = output.copy()
        panel_height = 80
        cv2.rectangle(overlay, (10, 10), (300, 10 + panel_height),
                     (0, 0, 0), -1)
        cv2.addWeighted(overlay, self.config['info_box_alpha'],
                       output, 1 - self.config['info_box_alpha'], 0, output)
        
        info_texts = [
            f"Frame: {frame_num}/{total_frames}",
            f"FPS: {fps:.1f}",
            f"Progress: {frame_num/total_frames*100:.1f}%"
        ]
        
        y_offset = 30
        for text in info_texts:
            cv2.putText(output, text, (20, y_offset),
                       self.config['text_font'],
                       self.config['text_scale'],
                       self.config['text_color'],
                       self.config['text_thickness'])
            y_offset += 20
        
        return output
    
    def visualize_pose(self, image: np.ndarray, results: object,
                      frame_num: int = 0, total_frames: int = 0,
                      fps: float = 30.0) -> np.ndarray:
        output = image.copy()
        
        h, w = image.shape[:2]
        landmarks = self.estimator.get_all_landmarks(results, (h, w))
        
        if landmarks:
            output = self.draw_skeleton(output, landmarks)
            output = self.draw_angles(output, landmarks)
        
        output = self.draw_info_panel(output, frame_num, total_frames, fps)
        
        return output

