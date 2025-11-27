"""
主程序入口：人体动作姿态估计与可视化系统
"""

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
    """确保必要的目录存在"""
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_video_files(directory: str) -> list:
    """
    获取目录下所有视频文件
    
    Args:
        directory: 目录路径
        
    Returns:
        视频文件路径列表
    """
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(Path(directory).glob(f'*{ext}'))
        video_files.extend(Path(directory).glob(f'*{ext.upper()}'))
    
    return [str(f) for f in video_files]


def process_single_video(input_path: str, output_path: str, 
                        complexity: int = 2, confidence: float = 0.5):
    """
    处理单个视频文件
    
    Args:
        input_path: 输入视频路径
        output_path: 输出视频路径
        complexity: 模型复杂度
        confidence: 检测置信度
    """
    print("="*60)
    print("人体动作姿态估计与可视化系统")
    print("="*60)
    print(f"\n输入文件: {input_path}")
    print(f"输出文件: {output_path}")
    print(f"模型复杂度: {complexity}")
    print(f"检测置信度: {confidence}")
    
    # 初始化组件
    print("\n初始化系统...")
    from config import MEDIAPIPE_CONFIG
    
    # 更新配置
    config = MEDIAPIPE_CONFIG.copy()
    config['model_complexity'] = complexity
    config['min_detection_confidence'] = confidence
    config['min_tracking_confidence'] = confidence
    
    estimator = PoseEstimator(config)
    visualizer = PoseVisualizer(estimator)
    processor = VideoProcessor(estimator, visualizer)
    
    # 处理视频
    print("开始处理视频...")
    success = processor.process_video(input_path, output_path)
    
    if success:
        print("✓ 处理成功！")
        print("="*60)
        return True
    else:
        print("✗ 处理失败！")
        print("="*60)
        return False


def batch_process(complexity: int = 2, confidence: float = 0.5):
    """
    批量处理视频文件
    
    Args:
        complexity: 模型复杂度
        confidence: 检测置信度
    """
    print("="*60)
    print("批量处理模式")
    print("="*60)
    
    # 获取输入文件夹中的所有视频
    video_files = get_video_files(INPUT_DIR)
    
    if not video_files:
        print(f"\n错误：在 '{INPUT_DIR}' 文件夹中未找到视频文件")
        print("请将视频文件放入该文件夹后重试")
        return
    
    print(f"\n找到 {len(video_files)} 个视频文件:")
    for i, video in enumerate(video_files, 1):
        print(f"  {i}. {os.path.basename(video)}")
    
    print("\n开始批量处理...\n")
    
    success_count = 0
    fail_count = 0
    
    for i, input_path in enumerate(video_files, 1):
        print(f"\n处理视频 {i}/{len(video_files)}: {os.path.basename(input_path)}")
        print("-"*60)
        
        # 生成输出文件名
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(OUTPUT_DIR, f"{name}_pose{ext}")
        
        # 处理视频
        if process_single_video(input_path, output_path, complexity, confidence):
            success_count += 1
        else:
            fail_count += 1
    
    # 输出统计
    print("\n" + "="*60)
    print("批量处理完成!")
    print(f"  成功: {success_count} 个视频")
    if fail_count > 0:
        print(f"  失败: {fail_count} 个视频")
    print("="*60)


def main():
    """主函数"""
    args = parse_arguments()
    
    # 确保目录存在
    ensure_directories()
    
    try:
        if args.batch:
            # 批量处理模式
            batch_process(args.complexity, args.confidence)
        elif args.input and args.output:
            # 单文件处理模式
            process_single_video(args.input, args.output, 
                               args.complexity, args.confidence)
        else:
            # 交互式模式
            print("="*60)
            print("人体动作姿态估计与可视化系统")
            print("="*60)
            print("\n请选择运行模式:")
            print("1. 处理单个视频文件")
            print("2. 批量处理input文件夹下的所有视频")
            print("3. 退出")
            
            choice = input("\n请输入选项 (1/2/3): ").strip()
            
            if choice == '1':
                input_path = input("请输入视频文件路径: ").strip()
                output_path = input("请输入输出文件路径: ").strip()
                
                if not output_path:
                    # 自动生成输出路径
                    filename = os.path.basename(input_path)
                    name, ext = os.path.splitext(filename)
                    output_path = os.path.join(OUTPUT_DIR, f"{name}_pose{ext}")
                
                process_single_video(input_path, output_path,
                                   args.complexity, args.confidence)
            
            elif choice == '2':
                batch_process(args.complexity, args.confidence)
            
            elif choice == '3':
                print("退出程序")
                sys.exit(0)
            
            else:
                print("无效的选项！")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

