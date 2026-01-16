"""
Preprocessing utilities for media files
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
import os
import tempfile


def extract_frames(video_path: str, max_frames: int = 30, 
                   target_size: Optional[Tuple[int, int]] = None) -> List[np.ndarray]:
    """
    Extract frames from video file.
    
    Args:
        video_path: Path to video file
        max_frames: Maximum number of frames to extract
        target_size: Optional (width, height) to resize frames
    
    Returns:
        List of frames as numpy arrays
    """
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate frame indices to extract (evenly spaced)
    if total_frames <= max_frames:
        frame_indices = range(total_frames)
    else:
        frame_indices = np.linspace(0, total_frames - 1, max_frames, dtype=int)
    
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        
        if ret:
            if target_size:
                frame = cv2.resize(frame, target_size)
            frames.append(frame)
    
    cap.release()
    return frames


def preprocess_video(video_path: str, output_path: Optional[str] = None,
                     max_duration: float = 30.0, target_fps: int = 30) -> str:
    """
    Preprocess video for analysis.
    - Limit duration
    - Normalize FPS
    - Ensure standard format
    
    Args:
        video_path: Input video path
        output_path: Optional output path (creates temp file if None)
        max_duration: Maximum video duration in seconds
        target_fps: Target frames per second
    
    Returns:
        Path to preprocessed video
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    
    # Get video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Calculate max frames based on duration
    max_frames = int(max_duration * target_fps)
    
    # Create output path if not provided
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix='.mp4')
        os.close(fd)
    
    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, target_fps, (width, height))
    
    # Calculate frame skip for target FPS
    frame_skip = max(1, int(original_fps / target_fps))
    
    frame_count = 0
    written_frames = 0
    
    while cap.isOpened() and written_frames < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_skip == 0:
            out.write(frame)
            written_frames += 1
        
        frame_count += 1
    
    cap.release()
    out.release()
    
    return output_path


def preprocess_audio(audio_path: str, output_path: Optional[str] = None,
                     target_sr: int = 22050, max_duration: float = 60.0) -> str:
    """
    Preprocess audio for analysis.
    - Resample to target sample rate
    - Limit duration
    - Normalize amplitude
    
    Args:
        audio_path: Input audio path
        output_path: Optional output path
        target_sr: Target sample rate
        max_duration: Maximum audio duration in seconds
    
    Returns:
        Path to preprocessed audio
    """
    try:
        import librosa
        import soundfile as sf
    except ImportError:
        raise ImportError("librosa and soundfile are required for audio preprocessing")
    
    # Load audio
    y, sr = librosa.load(audio_path, sr=target_sr, mono=True, duration=max_duration)
    
    # Normalize
    if np.max(np.abs(y)) > 0:
        y = y / np.max(np.abs(y)) * 0.9
    
    # Create output path if not provided
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix='.wav')
        os.close(fd)
    
    # Save preprocessed audio
    sf.write(output_path, y, target_sr)
    
    return output_path


def extract_audio_from_video(video_path: str, output_path: Optional[str] = None) -> str:
    """
    Extract audio track from video file.
    
    Args:
        video_path: Path to video file
        output_path: Optional output audio path
    
    Returns:
        Path to extracted audio file
    """
    try:
        import subprocess
    except ImportError:
        raise ImportError("subprocess module required")
    
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix='.wav')
        os.close(fd)
    
    # Try using ffmpeg if available
    try:
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn', '-acodec', 'pcm_s16le',
            '-ar', '22050', '-ac', '1',
            '-y', output_path
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        return output_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: return None if ffmpeg not available
        return None


def get_video_info(video_path: str) -> dict:
    """Get video file information"""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    
    info = {
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS),
        'codec': int(cap.get(cv2.CAP_PROP_FOURCC))
    }
    
    cap.release()
    return info


def get_audio_info(audio_path: str) -> dict:
    """Get audio file information"""
    try:
        import librosa
    except ImportError:
        raise ImportError("librosa is required for audio info")
    
    y, sr = librosa.load(audio_path, sr=None, mono=False)
    
    if len(y.shape) == 1:
        channels = 1
        samples = len(y)
    else:
        channels = y.shape[0]
        samples = y.shape[1]
    
    return {
        'sample_rate': sr,
        'channels': channels,
        'samples': samples,
        'duration': samples / sr
    }
