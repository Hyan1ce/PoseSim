"""
可视化模块：在视频帧上绘制骨架和参数标注
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
from config import VISUALIZATION_CONFIG, POSE_CONNECTIONS, ANGLES_TO_DISPLAY
from pose_estimator import PoseEstimator


class PoseVisualizer:
    """姿态可视化器"""
    
    def __init__(self, pose_estimator: PoseEstimator, config: Optional[Dict] = None):
        """
        初始化可视化器
        
        Args:
            pose_estimator: 姿态估计器实例
            config: 可视化配置，如果为None则使用默认配置
        """
        self.estimator = pose_estimator
        self.config = config or VISUALIZATION_CONFIG
    
    def draw_skeleton(self, image: np.ndarray, 
                     landmarks: Dict[str, Tuple[int, int]]) -> np.ndarray:
        """
        在图像上绘制火柴人骨架
        
        Args:
            image: 输入图像
            landmarks: 关键点坐标字典
            
        Returns:
            绘制后的图像
        """
        output = image.copy()
        
        # 绘制骨架连接线
        for connection in POSE_CONNECTIONS:
            point1_name, point2_name = connection
            
            if point1_name in landmarks and point2_name in landmarks:
                point1 = landmarks[point1_name]
                point2 = landmarks[point2_name]
                
                cv2.line(output, point1, point2,
                        self.config['skeleton_color'],
                        self.config['skeleton_thickness'])
        
        # 绘制关键点
        for point_name, coords in landmarks.items():
            cv2.circle(output, coords,
                      self.config['landmark_radius'],
                      self.config['landmark_color'],
                      -1)
        
        return output
    
    def draw_angle_arc(self, image: np.ndarray, center: Tuple[int, int],
                      angle: float, start_point: Tuple[int, int],
                      end_point: Tuple[int, int]) -> np.ndarray:
        """
        在关节处绘制角度弧线
        
        Args:
            image: 输入图像
            center: 角度顶点坐标
            angle: 角度值
            start_point: 起始点
            end_point: 结束点
            
        Returns:
            绘制后的图像
        """
        # 计算起始和结束角度
        start_vector = np.array(start_point) - np.array(center)
        end_vector = np.array(end_point) - np.array(center)
        
        start_angle = np.degrees(np.arctan2(start_vector[1], start_vector[0]))
        end_angle = np.degrees(np.arctan2(end_vector[1], end_vector[0]))
        
        # 绘制弧线
        radius = self.config['angle_arc_radius']
        cv2.ellipse(image, center, (radius, radius), 0,
                   start_angle, end_angle,
                   self.config['angle_color'], 2)
        
        return image
    
    def draw_angles(self, image: np.ndarray,
                   landmarks: Dict[str, Tuple[int, int]]) -> np.ndarray:
        """
        在图像上标注关节角度
        
        Args:
            image: 输入图像
            landmarks: 关键点坐标字典
            
        Returns:
            绘制后的图像
        """
        output = image.copy()
        
        for angle_info in ANGLES_TO_DISPLAY:
            point_names = angle_info['points']
            
            # 检查所有需要的点是否存在
            if all(name in landmarks for name in point_names):
                point1 = landmarks[point_names[0]]
                point2 = landmarks[point_names[1]]
                point3 = landmarks[point_names[2]]
                
                # 计算角度
                angle = self.estimator.calculate_angle(point1, point2, point3)
                
                # 获取标注位置
                label_pos = landmarks[angle_info['position']]
                
                # 绘制角度弧线（可选）
                # self.draw_angle_arc(output, point2, angle, point1, point3)
                
                # 绘制角度文字
                text = f"{angle:.1f}°"
                
                # 添加背景框使文字更清晰
                text_size = cv2.getTextSize(text, self.config['text_font'],
                                           self.config['text_scale'],
                                           self.config['text_thickness'])[0]
                
                # 调整文字位置，避免遮挡关键点
                text_x = label_pos[0] + 15
                text_y = label_pos[1] - 15
                
                # 绘制半透明背景
                overlay = output.copy()
                cv2.rectangle(overlay,
                            (text_x - 2, text_y - text_size[1] - 2),
                            (text_x + text_size[0] + 2, text_y + 2),
                            (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.6, output, 0.4, 0, output)
                
                # 绘制文字
                cv2.putText(output, text,
                          (text_x, text_y),
                          self.config['text_font'],
                          self.config['text_scale'],
                          self.config['angle_color'],
                          self.config['text_thickness'])
        
        return output
    
    def draw_info_panel(self, image: np.ndarray, frame_num: int,
                       total_frames: int, fps: float) -> np.ndarray:
        """
        绘制信息面板
        
        Args:
            image: 输入图像
            frame_num: 当前帧号
            total_frames: 总帧数
            fps: 帧率
            
        Returns:
            绘制后的图像
        """
        output = image.copy()
        h, w = output.shape[:2]
        
        # 创建半透明背景
        overlay = output.copy()
        panel_height = 80
        cv2.rectangle(overlay, (10, 10), (300, 10 + panel_height),
                     (0, 0, 0), -1)
        cv2.addWeighted(overlay, self.config['info_box_alpha'],
                       output, 1 - self.config['info_box_alpha'], 0, output)
        
        # 绘制文字信息
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
        """
        完整的姿态可视化流程
        
        Args:
            image: 输入图像
            results: MediaPipe姿态估计结果
            frame_num: 当前帧号
            total_frames: 总帧数
            fps: 帧率
            
        Returns:
            可视化后的图像
        """
        output = image.copy()
        
        # 获取所有关键点坐标
        h, w = image.shape[:2]
        landmarks = self.estimator.get_all_landmarks(results, (h, w))
        
        if landmarks:
            # 绘制骨架
            output = self.draw_skeleton(output, landmarks)
            
            # 绘制角度标注
            output = self.draw_angles(output, landmarks)
        
        # 绘制信息面板
        output = self.draw_info_panel(output, frame_num, total_frames, fps)
        
        return output

