import os
import sys
import argparse
from pathlib import Path
from pose_estimator import PoseEstimator
from visualizer import PoseVisualizer
from video_processor import VideoProcessor
from config import INPUT_DIR, OUTPUT_DIR


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='人体动作姿态估计与可视化系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 处理单个视频文件
  python main.py -i input/dance.mp4 -o output/dance_pose.mp4
  
  # 处理input文件夹下的所有视频
  python main.py --batch
  
  # 指定MediaPipe模型复杂度（0=最快，1=平衡，2=最准）
  python main.py -i input/video.mp4 -o output/result.mp4 --complexity 1
        """
    )
    
    parser.add_argument('-i', '--input', type=str,
                       help='输入视频文件路径')
    parser.add_argument('-o', '--output', type=str,
                       help='输出视频文件路径')
    parser.add_argument('--batch', action='store_true',
                       help='批量处理input文件夹下的所有视频')
    parser.add_argument('--complexity', type=int, choices=[0, 1, 2], default=2,
                       help='MediaPipe模型复杂度 (0=快速, 1=平衡, 2=精确)')
    parser.add_argument('--confidence', type=float, default=0.5,
                       help='姿态检测最小置信度 (0.0-1.0)')
    
    return parser.parse_args()


def ensure_directories():
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_video_files(directory: str) -> list:
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(Path(directory).glob(f'*{ext}'))
        video_files.extend(Path(directory).glob(f'*{ext.upper()}'))
    
    return [str(f) for f in video_files]


def process_single_video(input_path: str, output_path: str, 
                        complexity: int = 2, confidence: float = 0.5):
    print("="*60)
    print("Pose Estimation and Visualization System")
    print("="*60)
    print(f"\nInput file: {input_path}")
    print(f"Output file: {output_path}")
    print(f"Model complexity: {complexity}")
    print(f"Detection confidence: {confidence}")
    
    print("\nInitializing system")
    from config import MEDIAPIPE_CONFIG
    
    config = MEDIAPIPE_CONFIG.copy()
    config['model_complexity'] = complexity
    config['min_detection_confidence'] = confidence
    config['min_tracking_confidence'] = confidence
    
    estimator = PoseEstimator(config)
    visualizer = PoseVisualizer(estimator)
    processor = VideoProcessor(estimator, visualizer)
    
    print("Processing video")
    success = processor.process_video(input_path, output_path)
    
    if success:
        print("Processing completed successfully")
        print("="*60)
        return True
    else:
        print("Processing failed")
        print("="*60)
        return False


def batch_process(complexity: int = 2, confidence: float = 0.5):
    print("="*60)
    print("Batch Processing Mode")
    print("="*60)
    
    video_files = get_video_files(INPUT_DIR)
    
    if not video_files:
        print(f"\nError: No video files found in '{INPUT_DIR}'")
        print("Please add video files to the folder and retry")
        return
    
    print(f"\nFound {len(video_files)} video files:")
    for i, video in enumerate(video_files, 1):
        print(f"  {i}. {os.path.basename(video)}")
    
    print("\nStarting batch processing\n")
    
    success_count = 0
    fail_count = 0
    
    for i, input_path in enumerate(video_files, 1):
        print(f"\nProcessing video {i}/{len(video_files)}: {os.path.basename(input_path)}")
        print("-"*60)
        
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(OUTPUT_DIR, f"{name}_pose{ext}")
        
        if process_single_video(input_path, output_path, complexity, confidence):
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "="*60)
    print("Batch processing completed")
    print(f"  Success: {success_count} videos")
    if fail_count > 0:
        print(f"  Failed: {fail_count} videos")
    print("="*60)


def main():
    args = parse_arguments()
    
    ensure_directories()
    
    try:
        if args.batch:
            batch_process(args.complexity, args.confidence)
        elif args.input and args.output:
            process_single_video(args.input, args.output, 
                               args.complexity, args.confidence)
        else:
            print("="*60)
            print("Pose Estimation and Visualization System")
            print("="*60)
            print("\nPlease select a mode:")
            print("1. Process single video file")
            print("2. Batch process all videos in input folder")
            print("3. Exit")
            
            choice = input("\nEnter option (1/2/3): ").strip()
            
            if choice == '1':
                input_path = input("Enter video file path: ").strip()
                output_path = input("Enter output file path: ").strip()
                
                if not output_path:
                    filename = os.path.basename(input_path)
                    name, ext = os.path.splitext(filename)
                    output_path = os.path.join(OUTPUT_DIR, f"{name}_pose{ext}")
                
                process_single_video(input_path, output_path,
                                   args.complexity, args.confidence)
            
            elif choice == '2':
                batch_process(args.complexity, args.confidence)
            
            elif choice == '3':
                print("Exiting program")
                sys.exit(0)
            
            else:
                print("Invalid option")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

