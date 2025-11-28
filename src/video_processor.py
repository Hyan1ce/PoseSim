import cv2
import os
from typing import Optional
from tqdm import tqdm
from pose_estimator import PoseEstimator
from visualizer import PoseVisualizer
from config import VIDEO_CONFIG


class VideoProcessor:
    
    def __init__(self, pose_estimator: PoseEstimator, visualizer: PoseVisualizer):
        self.estimator = pose_estimator
        self.visualizer = visualizer
        self.config = VIDEO_CONFIG
    
    def process_video(self, input_path: str, output_path: str) -> bool:
        if not os.path.exists(input_path):
            print(f"Error: Input video file does not exist: {input_path}")
            return False
        
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Cannot open video file: {input_path}")
            return False
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"\nVideo information:")
        print(f"  Resolution: {width}x{height}")
        print(f"  Frame rate: {fps:.2f} FPS")
        print(f"  Total frames: {total_frames}")
        print(f"  Duration: {total_frames/fps:.2f} seconds\n")
        
        output_fps = self.config['output_fps'] or fps
        
        fourcc = cv2.VideoWriter_fourcc(*self.config['output_codec'])
        out = cv2.VideoWriter(output_path, fourcc, output_fps, (width, height))
        
        if not out.isOpened():
            print(f"Error: Cannot create output video file: {output_path}")
            cap.release()
            return False
        
        frame_num = 0
        
        if self.config['show_progress']:
            pbar = tqdm(total=total_frames, desc="Processing", unit="frames")
        
        success_count = 0
        fail_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                break
            
            frame_num += 1
            
            try:
                results = self.estimator.estimate(frame)
                output_frame = self.visualizer.visualize_pose(
                    frame, results, frame_num, total_frames, fps
                )
                out.write(output_frame)
                success_count += 1
                
            except Exception as e:
                print(f"\nWarning: Error processing frame {frame_num}: {str(e)}")
                out.write(frame)
                fail_count += 1
            
            if self.config['show_progress']:
                pbar.update(1)
        
        if self.config['show_progress']:
            pbar.close()
        
        cap.release()
        out.release()
        
        print(f"\nProcessing completed")
        print(f"  Successfully processed: {success_count} frames")
        if fail_count > 0:
            print(f"  Failed: {fail_count} frames")
        print(f"  Output file: {output_path}\n")
        
        return True
    
    def process_frame(self, frame) -> Optional[object]:
        try:
            results = self.estimator.estimate(frame)
            output_frame = self.visualizer.visualize_pose(frame, results)
            return output_frame
        except Exception as e:
            print(f"Error processing frame: {str(e)}")
            return None
    
    def get_video_info(self, video_path: str) -> Optional[dict]:
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

