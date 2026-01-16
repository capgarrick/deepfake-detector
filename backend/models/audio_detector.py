"""
Audio Deepfake Detector
Uses spectral analysis to detect synthetic or manipulated audio
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
import os

# Try to import audio libraries
try:
    import librosa
    import librosa.display
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

try:
    from scipy import signal
    from scipy.stats import kurtosis, skew
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


class AudioDeepfakeDetector:
    """
    Spectral analysis-based deepfake detection for audio content.
    Analyzes:
    - MFCC (Mel-frequency cepstral coefficients)
    - Spectral features (centroid, bandwidth, rolloff)
    - Temporal patterns
    - Voice naturalness indicators
    """
    
    def __init__(self):
        self.sample_rate = 22050
        self.n_mfcc = 20
        self.hop_length = 512
        self.n_fft = 2048
        
    def load_audio(self, audio_path: str) -> Tuple[np.ndarray, int]:
        """Load audio file and return waveform with sample rate"""
        if not LIBROSA_AVAILABLE:
            raise ImportError("librosa is required for audio analysis. Install with: pip install librosa")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Load audio with librosa
        y, sr = librosa.load(audio_path, sr=self.sample_rate, mono=True)
        return y, sr
    
    def extract_mfcc_features(self, y: np.ndarray, sr: int) -> Dict:
        """
        Extract MFCC features - crucial for detecting synthetic speech.
        AI-generated audio often has different MFCC patterns.
        """
        if not LIBROSA_AVAILABLE:
            return {'error': 'librosa not available'}
        
        # Extract MFCCs
        mfccs = librosa.feature.mfcc(
            y=y, 
            sr=sr, 
            n_mfcc=self.n_mfcc,
            hop_length=self.hop_length,
            n_fft=self.n_fft
        )
        
        # Calculate statistics for each coefficient
        mfcc_mean = np.mean(mfccs, axis=1)
        mfcc_std = np.std(mfccs, axis=1)
        mfcc_delta = librosa.feature.delta(mfccs)
        mfcc_delta_mean = np.mean(mfcc_delta, axis=1)
        
        # Synthetic audio often has smoother MFCC transitions
        mfcc_variance = np.var(mfccs, axis=1)
        smoothness_score = 1 - min(1, np.mean(mfcc_variance) / 100)
        
        return {
            'mfcc_mean': mfcc_mean.tolist(),
            'mfcc_std': mfcc_std.tolist(),
            'delta_mean': mfcc_delta_mean.tolist(),
            'smoothness_score': smoothness_score,
            'coefficient_variance': np.mean(mfcc_variance)
        }
    
    def extract_spectral_features(self, y: np.ndarray, sr: int) -> Dict:
        """
        Extract spectral features that help identify synthetic audio.
        """
        if not LIBROSA_AVAILABLE:
            return {'error': 'librosa not available'}
        
        # Spectral centroid - "brightness" of sound
        spectral_centroids = librosa.feature.spectral_centroid(
            y=y, sr=sr, hop_length=self.hop_length
        )[0]
        
        # Spectral bandwidth
        spectral_bandwidth = librosa.feature.spectral_bandwidth(
            y=y, sr=sr, hop_length=self.hop_length
        )[0]
        
        # Spectral rolloff - frequency below which most energy is contained
        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=y, sr=sr, hop_length=self.hop_length
        )[0]
        
        # Spectral flatness - how noise-like vs tone-like
        spectral_flatness = librosa.feature.spectral_flatness(
            y=y, hop_length=self.hop_length
        )[0]
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y, hop_length=self.hop_length)[0]
        
        # Calculate anomaly indicators
        centroid_variance = np.var(spectral_centroids)
        bandwidth_variance = np.var(spectral_bandwidth)
        
        # Synthetic audio often has more consistent spectral properties
        spectral_consistency = 1 - min(1, centroid_variance / 1e6)
        
        return {
            'centroid_mean': float(np.mean(spectral_centroids)),
            'centroid_std': float(np.std(spectral_centroids)),
            'bandwidth_mean': float(np.mean(spectral_bandwidth)),
            'rolloff_mean': float(np.mean(spectral_rolloff)),
            'flatness_mean': float(np.mean(spectral_flatness)),
            'zcr_mean': float(np.mean(zcr)),
            'spectral_consistency': spectral_consistency
        }
    
    def analyze_temporal_patterns(self, y: np.ndarray, sr: int) -> Dict:
        """
        Analyze temporal patterns in audio.
        Real speech has natural rhythm and pauses.
        """
        if not LIBROSA_AVAILABLE:
            return {'error': 'librosa not available'}
        
        # Get onset envelope
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        
        # Tempo estimation
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        
        # RMS energy
        rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]
        
        # Analyze silence patterns
        silence_threshold = np.max(rms) * 0.1
        silence_frames = np.sum(rms < silence_threshold)
        silence_ratio = silence_frames / len(rms)
        
        # Calculate energy variation
        energy_variance = np.var(rms)
        
        # Synthetic audio often has unnatural rhythm
        rhythm_score = min(1, len(beats) / (len(y) / sr / 2))  # Expected ~2 beats per second speech
        
        return {
            'tempo': float(tempo) if np.isscalar(tempo) else float(tempo[0]) if len(tempo) > 0 else 0.0,
            'num_beats': len(beats),
            'silence_ratio': float(silence_ratio),
            'energy_variance': float(energy_variance),
            'rhythm_naturalness': float(rhythm_score)
        }
    
    def analyze_voice_quality(self, y: np.ndarray, sr: int) -> Dict:
        """
        Analyze voice quality indicators.
        Synthetic voices often lack natural micro-variations.
        """
        if not LIBROSA_AVAILABLE or not SCIPY_AVAILABLE:
            return {'error': 'Required libraries not available'}
        
        # Pitch (F0) analysis
        pitches, magnitudes = librosa.piptrack(
            y=y, sr=sr, hop_length=self.hop_length
        )
        
        # Get valid pitches
        valid_pitches = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                valid_pitches.append(pitch)
        
        if len(valid_pitches) > 0:
            pitch_mean = np.mean(valid_pitches)
            pitch_std = np.std(valid_pitches)
            pitch_range = np.max(valid_pitches) - np.min(valid_pitches)
        else:
            pitch_mean = 0
            pitch_std = 0
            pitch_range = 0
        
        # Jitter (pitch variation) - natural voices have micro-jitter
        if len(valid_pitches) > 1:
            pitch_diffs = np.diff(valid_pitches)
            jitter = np.std(pitch_diffs) / (pitch_mean + 1e-6)
        else:
            jitter = 0
        
        # Shimmer (amplitude variation)
        amplitude = np.abs(y)
        if len(amplitude) > 1:
            amp_diffs = np.diff(amplitude[::100])  # Subsample
            shimmer = np.std(amp_diffs) / (np.mean(amplitude) + 1e-6)
        else:
            shimmer = 0
        
        # Natural voices have moderate jitter and shimmer
        voice_naturalness = min(1, (jitter * 10 + shimmer) / 2)
        
        return {
            'pitch_mean': float(pitch_mean),
            'pitch_std': float(pitch_std),
            'pitch_range': float(pitch_range),
            'jitter': float(jitter),
            'shimmer': float(shimmer),
            'voice_naturalness': float(voice_naturalness)
        }
    
    def detect_artifacts(self, y: np.ndarray, sr: int) -> Dict:
        """
        Detect audio artifacts common in synthetic audio:
        - Unnatural frequency gaps
        - Periodic patterns from vocoders
        - Boundary artifacts from concatenation
        """
        if not LIBROSA_AVAILABLE:
            return {'error': 'librosa not available'}
        
        # Compute spectrogram
        D = librosa.stft(y, n_fft=self.n_fft, hop_length=self.hop_length)
        S = np.abs(D)
        
        # Check for frequency gaps (common in low-quality synthesis)
        freq_energy = np.mean(S, axis=1)
        freq_gaps = np.sum(freq_energy < np.max(freq_energy) * 0.01)
        gap_ratio = freq_gaps / len(freq_energy)
        
        # Check for periodic patterns (vocoder artifacts)
        autocorr = np.correlate(freq_energy, freq_energy, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        peaks = self._find_peaks(autocorr)
        periodicity_score = len(peaks) / 10  # Normalize
        
        # Check for concatenation artifacts (sudden spectral changes)
        spectral_diff = np.diff(S, axis=1)
        large_changes = np.sum(np.abs(spectral_diff) > np.std(spectral_diff) * 3)
        concat_score = large_changes / spectral_diff.size * 100
        
        artifact_score = (gap_ratio + periodicity_score + concat_score) / 3
        
        return {
            'frequency_gaps': float(gap_ratio),
            'periodicity': float(periodicity_score),
            'concatenation_artifacts': float(concat_score),
            'overall_artifact_score': float(min(1, artifact_score))
        }
    
    def _find_peaks(self, arr: np.ndarray, threshold: float = 0.5) -> List[int]:
        """Find peaks in array above threshold of max"""
        max_val = np.max(arr)
        peaks = []
        for i in range(1, len(arr) - 1):
            if arr[i] > arr[i-1] and arr[i] > arr[i+1] and arr[i] > max_val * threshold:
                peaks.append(i)
        return peaks
    
    def analyze_audio(self, audio_path: str) -> Dict:
        """
        Perform complete deepfake analysis on audio.
        Returns detection results with confidence scores.
        """
        try:
            # Load audio
            y, sr = self.load_audio(audio_path)
            
            # Duration check
            duration = len(y) / sr
            if duration < 0.5:
                return {
                    'success': False,
                    'error': 'Audio too short (minimum 0.5 seconds)',
                    'duration': duration
                }
            
            # Extract all features
            mfcc_features = self.extract_mfcc_features(y, sr)
            spectral_features = self.extract_spectral_features(y, sr)
            temporal_features = self.analyze_temporal_patterns(y, sr)
            voice_features = self.analyze_voice_quality(y, sr)
            artifact_features = self.detect_artifacts(y, sr)
            
            # Calculate composite scores
            smoothness = mfcc_features.get('smoothness_score', 0.5)
            spectral_consistency = spectral_features.get('spectral_consistency', 0.5)
            rhythm_naturalness = temporal_features.get('rhythm_naturalness', 0.5)
            voice_naturalness = voice_features.get('voice_naturalness', 0.5)
            artifact_score = artifact_features.get('overall_artifact_score', 0.5)
            
            # Weighted deepfake probability
            # Higher smoothness + consistency = more likely synthetic
            # Lower naturalness = more likely synthetic
            deepfake_score = (
                smoothness * 0.25 +
                spectral_consistency * 0.20 +
                (1 - rhythm_naturalness) * 0.15 +
                (1 - voice_naturalness) * 0.20 +
                artifact_score * 0.20
            )
            
            is_deepfake = deepfake_score > 0.45
            authenticity = max(0, min(100, (1 - deepfake_score) * 100))
            
            # Confidence based on feature consistency
            confidence = min(90, max(55, 100 - abs(deepfake_score - 0.5) * 100))
            
            return {
                'success': True,
                'duration': round(duration, 2),
                'sample_rate': sr,
                'is_deepfake': is_deepfake,
                'deepfake_probability': round(deepfake_score * 100, 1),
                'authenticity_score': round(authenticity, 1),
                'confidence': round(confidence, 1),
                'details': {
                    'mfcc_smoothness': round(smoothness * 100, 1),
                    'spectral_consistency': round(spectral_consistency * 100, 1),
                    'rhythm_naturalness': round(rhythm_naturalness * 100, 1),
                    'voice_naturalness': round(voice_naturalness * 100, 1),
                    'artifact_level': round(artifact_score * 100, 1)
                },
                'voice_metrics': {
                    'pitch_mean': round(voice_features.get('pitch_mean', 0), 1),
                    'pitch_variation': round(voice_features.get('pitch_std', 0), 1),
                    'jitter': round(voice_features.get('jitter', 0) * 100, 2),
                    'shimmer': round(voice_features.get('shimmer', 0) * 100, 2)
                },
                'indicators': self._get_indicators(
                    smoothness, spectral_consistency, 
                    rhythm_naturalness, voice_naturalness, artifact_score
                )
            }
            
        except FileNotFoundError as e:
            return {'success': False, 'error': str(e)}
        except Exception as e:
            return {'success': False, 'error': f'Analysis failed: {str(e)}'}
    
    def _get_indicators(self, smoothness: float, spectral: float, 
                       rhythm: float, voice: float, artifacts: float) -> List[str]:
        """Generate human-readable indicators based on scores"""
        indicators = []
        
        if smoothness > 0.6:
            indicators.append("Unusually smooth audio characteristics (typical of synthesis)")
        if spectral > 0.6:
            indicators.append("Overly consistent spectral patterns detected")
        if rhythm < 0.4:
            indicators.append("Unnatural speech rhythm patterns")
        if voice < 0.4:
            indicators.append("Missing natural voice micro-variations")
        if artifacts > 0.5:
            indicators.append("Audio artifacts consistent with manipulation")
        
        if len(indicators) == 0:
            indicators.append("Audio exhibits natural speech characteristics")
        
        return indicators
