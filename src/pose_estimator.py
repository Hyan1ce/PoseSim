"""
姿态估计模块：使用MediaPipe进行人体姿态估计
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Dict, List, Tuple
from config import MEDIAPIPE_CONFIG


class PoseEstimator:
    """人体姿态估计器"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化姿态估计器
        
        Args:
            config: MediaPipe配置参数，如果为None则使用默认配置
        """
        self.config = config or MEDIAPIPE_CONFIG
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(**self.config)
        
        # 创建关键点名称到索引的映射
        self.landmark_names = [landmark.name for landmark in self.mp_pose.PoseLandmark]
        self.landmark_dict = {name: idx for idx, name in enumerate(self.landmark_names)}
    
    def estimate(self, image: np.ndarray) -> Optional[object]:
        """
        对单帧图像进行姿态估计
        
        Args:
            image: 输入图像 (BGR格式)
            
        Returns:
            MediaPipe姿态估计结果，如果检测失败则返回None
        """
        # 转换为RGB格式
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 提高性能：标记图像为不可写
        image_rgb.flags.writeable = False
        results = self.pose.process(image_rgb)
        image_rgb.flags.writeable = True
        
        return results
    
    def get_landmark_coords(self, results: object, landmark_name: str, 
                           image_shape: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        获取指定关键点的像素坐标
        
        Args:
            results: MediaPipe姿态估计结果
            landmark_name: 关键点名称
            image_shape: 图像尺寸 (height, width)
            
        Returns:
            关键点的(x, y)坐标，如果不存在则返回None
        """
        if not results.pose_landmarks:
            return None
        
        try:
            landmark_idx = self.landmark_dict[landmark_name]
            landmark = results.pose_landmarks.landmark[landmark_idx]
            
            # 转换归一化坐标到像素坐标
            h, w = image_shape
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            
            # 检查可见性
            if landmark.visibility < 0.5:
                return None
                
            return (x, y)
        except (KeyError, IndexError):
            return None
    
    def get_all_landmarks(self, results: object, 
                         image_shape: Tuple[int, int]) -> Dict[str, Tuple[int, int]]:
        """
        获取所有关键点的坐标
        
        Args:
            results: MediaPipe姿态估计结果
            image_shape: 图像尺寸 (height, width)
            
        Returns:
            关键点名称到坐标的字典
        """
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
        """
        计算三个点形成的角度
        
        Args:
            point1: 第一个点坐标
            point2: 顶点坐标（角的顶点）
            point3: 第三个点坐标
            
        Returns:
            角度值（度数）
        """
        # 转换为numpy数组
        p1 = np.array(point1)
        p2 = np.array(point2)
        p3 = np.array(point3)
        
        # 计算向量
        vector1 = p1 - p2
        vector2 = p3 - p2
        
        # 计算角度
        cos_angle = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = np.arccos(cos_angle)
        
        return np.degrees(angle)
    
    def calculate_distance(self, point1: Tuple[int, int], 
                          point2: Tuple[int, int]) -> float:
        """
        计算两点之间的欧氏距离
        
        Args:
            point1: 第一个点坐标
            point2: 第二个点坐标
            
        Returns:
            距离值（像素）
        """
        p1 = np.array(point1)
        p2 = np.array(point2)
        return np.linalg.norm(p1 - p2)
    
    def __del__(self):
        """清理资源"""
        self.pose.close()

