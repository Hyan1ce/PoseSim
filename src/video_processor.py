"""
视频处理模块：处理输入视频并生成带姿态标注的输出视频
"""

import cv2
import os
from typing import Optional
from tqdm import tqdm
from pose_estimator import PoseEstimator
from visualizer import PoseVisualizer
from config import VIDEO_CONFIG


class VideoProcessor:
    """视频处理器"""
    
    def __init__(self, pose_estimator: PoseEstimator, visualizer: PoseVisualizer):
        """
        初始化视频处理器
        
        Args:
            pose_estimator: 姿态估计器实例
            visualizer: 可视化器实例
        """
        self.estimator = pose_estimator
        self.visualizer = visualizer
        self.config = VIDEO_CONFIG
    
    def process_video(self, input_path: str, output_path: str) -> bool:
        """
        处理视频文件
        
        Args:
            input_path: 输入视频路径
            output_path: 输出视频路径
            
        Returns:
            处理是否成功
        """
        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            print(f"错误：输入视频文件不存在: {input_path}")
            return False
        
        # 打开输入视频
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"错误：无法打开视频文件: {input_path}")
            return False
        
        # 获取视频属性
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"\n视频信息:")
        print(f"  分辨率: {width}x{height}")
        print(f"  帧率: {fps:.2f} FPS")
        print(f"  总帧数: {total_frames}")
        print(f"  时长: {total_frames/fps:.2f} 秒\n")
        
        # 设置输出fps
        output_fps = self.config['output_fps'] or fps
        
        # 创建视频写入器
        fourcc = cv2.VideoWriter_fourcc(*self.config['output_codec'])
        out = cv2.VideoWriter(output_path, fourcc, output_fps, (width, height))
        
        if not out.isOpened():
            print(f"错误：无法创建输出视频文件: {output_path}")
            cap.release()
            return False
        
        # 处理视频帧
        frame_num = 0
        
        # 使用进度条
        if self.config['show_progress']:
            pbar = tqdm(total=total_frames, desc="处理进度", unit="帧")
        
        success_count = 0
        fail_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                break
            
            frame_num += 1
            
            try:
                # 姿态估计
                results = self.estimator.estimate(frame)
                
                # 可视化
                output_frame = self.visualizer.visualize_pose(
                    frame, results, frame_num, total_frames, fps
                )
                
                # 写入输出视频
                out.write(output_frame)
                success_count += 1
                
            except Exception as e:
                print(f"\n警告：处理第 {frame_num} 帧时出错: {str(e)}")
                # 出错时直接写入原始帧
                out.write(frame)
                fail_count += 1
            
            # 更新进度条
            if self.config['show_progress']:
                pbar.update(1)
        
        # 清理资源
        if self.config['show_progress']:
            pbar.close()
        
        cap.release()
        out.release()
        
        # 输出统计信息
        print(f"\n处理完成!")
        print(f"  成功处理: {success_count} 帧")
        if fail_count > 0:
            print(f"  处理失败: {fail_count} 帧")
        print(f"  输出文件: {output_path}\n")
        
        return True
    
    def process_frame(self, frame) -> Optional[object]:
        """
        处理单帧图像（用于实时处理或预览）
        
        Args:
            frame: 输入帧
            
        Returns:
            处理后的帧，如果失败则返回None
        """
        try:
            results = self.estimator.estimate(frame)
            output_frame = self.visualizer.visualize_pose(frame, results)
            return output_frame
        except Exception as e:
            print(f"处理帧时出错: {str(e)}")
            return None
    
    def get_video_info(self, video_path: str) -> Optional[dict]:
        """
        获取视频文件信息
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            视频信息字典，如果失败则返回None
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            return None
        
        info = {
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'duration': cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        }
        
        cap.release()
        return info

