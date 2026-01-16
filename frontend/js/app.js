/**
 * DeepGuard - Deepfake Detection System
 * Frontend JavaScript Application
 */

// Configuration - uses dynamic URL from config.js if available
const CONFIG = {
    API_BASE_URL: window.DEEPGUARD_API_URL || 'http://localhost:8000',
    MAX_FILE_SIZE: 100 * 1024 * 1024, // 100MB
    ALLOWED_VIDEO_TYPES: ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-msvideo', 'video/webm', 'video/x-matroska'],
    ALLOWED_AUDIO_TYPES: ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/flac', 'audio/x-m4a', 'audio/mp3']
};

// State
let state = {
    selectedFile: null,
    isAnalyzing: false,
    analysisType: 'full'
};

// DOM Elements
const elements = {
    uploadZone: document.getElementById('uploadZone'),
    fileInput: document.getElementById('fileInput'),
    uploadPreview: document.getElementById('uploadPreview'),
    previewIcon: document.getElementById('previewIcon'),
    previewName: document.getElementById('previewName'),
    previewSize: document.getElementById('previewSize'),
    removeFile: document.getElementById('removeFile'),
    analyzeBtn: document.getElementById('analyzeBtn'),
    analysisProgress: document.getElementById('analysisProgress'),
    progressFill: document.getElementById('progressFill'),
    resultsSection: document.getElementById('resultsSection'),
    newAnalysisBtn: document.getElementById('newAnalysisBtn'),
    scoreValue: document.getElementById('scoreValue'),
    scoreRing: document.getElementById('scoreRing'),
    verdictBadge: document.getElementById('verdictBadge'),
    verdictIcon: document.getElementById('verdictIcon'),
    verdictText: document.getElementById('verdictText'),
    scoreDescription: document.getElementById('scoreDescription'),
    confidenceFill: document.getElementById('confidenceFill'),
    confidenceValue: document.getElementById('confidenceValue'),
    detailsGrid: document.getElementById('detailsGrid'),
    indicatorsList: document.getElementById('indicatorsList'),
    tipsList: document.getElementById('tipsList')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    addSVGGradient();
    initSmoothScroll();
});

/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
    // Upload zone events
    elements.uploadZone.addEventListener('click', () => elements.fileInput.click());
    elements.uploadZone.addEventListener('dragover', handleDragOver);
    elements.uploadZone.addEventListener('dragleave', handleDragLeave);
    elements.uploadZone.addEventListener('drop', handleDrop);
    elements.fileInput.addEventListener('change', handleFileSelect);
    elements.removeFile.addEventListener('click', handleRemoveFile);

    // Analysis options
    document.querySelectorAll('input[name="analysisType"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            state.analysisType = e.target.value;
        });
    });

    // Analyze button
    elements.analyzeBtn.addEventListener('click', handleAnalyze);

    // New analysis button
    elements.newAnalysisBtn.addEventListener('click', resetToInitialState);

    // Navigation smooth scroll
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', handleNavClick);
    });
}

/**
 * Add SVG gradient for score ring
 */
function addSVGGradient() {
    const svg = document.querySelector('.score-ring');
    if (svg) {
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        defs.innerHTML = `
            <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#7C3AED"/>
                <stop offset="100%" style="stop-color:#06B6D4"/>
            </linearGradient>
        `;
        svg.insertBefore(defs, svg.firstChild);
    }
}

/**
 * Initialize smooth scrolling
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

/**
 * Handle navigation click
 */
function handleNavClick(e) {
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    e.target.classList.add('active');
}

/**
 * Handle drag over event
 */
function handleDragOver(e) {
    e.preventDefault();
    elements.uploadZone.classList.add('dragover');
}

/**
 * Handle drag leave event
 */
function handleDragLeave(e) {
    e.preventDefault();
    elements.uploadZone.classList.remove('dragover');
}

/**
 * Handle file drop
 */
function handleDrop(e) {
    e.preventDefault();
    elements.uploadZone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

/**
 * Handle file selection from input
 */
function handleFileSelect(e) {
    if (e.target.files.length > 0) {
        processFile(e.target.files[0]);
    }
}

/**
 * Process selected file
 */
function processFile(file) {
    // Validate file type
    const isVideo = CONFIG.ALLOWED_VIDEO_TYPES.some(type =>
        file.type === type || file.name.toLowerCase().endsWith('.mp4') ||
        file.name.toLowerCase().endsWith('.avi') || file.name.toLowerCase().endsWith('.mov') ||
        file.name.toLowerCase().endsWith('.mkv') || file.name.toLowerCase().endsWith('.webm')
    );
    const isAudio = CONFIG.ALLOWED_AUDIO_TYPES.some(type =>
        file.type === type || file.name.toLowerCase().endsWith('.mp3') ||
        file.name.toLowerCase().endsWith('.wav') || file.name.toLowerCase().endsWith('.ogg') ||
        file.name.toLowerCase().endsWith('.flac') || file.name.toLowerCase().endsWith('.m4a')
    );

    if (!isVideo && !isAudio) {
        showError('Invalid file type. Please upload a video or audio file.');
        return;
    }

    // Validate file size
    if (file.size > CONFIG.MAX_FILE_SIZE) {
        showError('File too large. Maximum size is 100MB.');
        return;
    }

    state.selectedFile = file;

    // Update preview
    elements.previewIcon.textContent = isVideo ? '🎬' : '🎵';
    elements.previewName.textContent = file.name;
    elements.previewSize.textContent = formatFileSize(file.size);

    // Show preview, hide upload content
    document.querySelector('.upload-content').style.display = 'none';
    elements.uploadPreview.hidden = false;

    // Enable analyze button
    elements.analyzeBtn.disabled = false;

    // Auto-select appropriate analysis type for audio files
    if (isAudio && !isVideo) {
        document.querySelector('input[value="audio"]').checked = true;
        state.analysisType = 'audio';
    }
}

/**
 * Handle remove file button
 */
function handleRemoveFile(e) {
    e.stopPropagation();
    state.selectedFile = null;
    elements.fileInput.value = '';

    // Reset UI
    document.querySelector('.upload-content').style.display = 'block';
    elements.uploadPreview.hidden = true;
    elements.analyzeBtn.disabled = true;
}

/**
 * Handle analyze button click
 */
async function handleAnalyze() {
    if (!state.selectedFile || state.isAnalyzing) return;

    state.isAnalyzing = true;

    // Update UI for loading state
    elements.analyzeBtn.querySelector('.btn-text').classList.add('hidden');
    elements.analyzeBtn.querySelector('.btn-loader').classList.remove('hidden');
    elements.analyzeBtn.disabled = true;
    elements.analysisProgress.classList.remove('hidden');
    elements.resultsSection.classList.add('hidden');

    // Progress animation
    updateProgress(0, 1);

    try {
        // Determine endpoint
        let endpoint;
        switch (state.analysisType) {
            case 'video':
                endpoint = '/api/analyze/video';
                break;
            case 'audio':
                endpoint = '/api/analyze/audio';
                break;
            default:
                endpoint = '/api/analyze/full';
        }

        // Create form data
        const formData = new FormData();
        formData.append('file', state.selectedFile);

        // Update progress
        updateProgress(30, 2);

        // Make API request
        const response = await fetch(CONFIG.API_BASE_URL + endpoint, {
            method: 'POST',
            body: formData
        });

        updateProgress(70, 2);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed');
        }

        const result = await response.json();

        updateProgress(100, 3);

        // Short delay to show completed progress
        await sleep(500);

        // Display results
        displayResults(result);

    } catch (error) {
        console.error('Analysis error:', error);
        showError(error.message || 'Failed to analyze file. Please try again.');
        resetAnalysisUI();
    } finally {
        state.isAnalyzing = false;
    }
}

/**
 * Update progress bar and steps
 */
function updateProgress(percent, step) {
    elements.progressFill.style.width = `${percent}%`;

    for (let i = 1; i <= 3; i++) {
        const stepEl = document.getElementById(`step${i}`);
        if (i < step) {
            stepEl.classList.add('completed');
            stepEl.classList.remove('active');
        } else if (i === step) {
            stepEl.classList.add('active');
            stepEl.classList.remove('completed');
        } else {
            stepEl.classList.remove('active', 'completed');
        }
    }
}

/**
 * Display analysis results
 */
function displayResults(result) {
    // Hide progress, show results
    elements.analysisProgress.classList.add('hidden');
    elements.resultsSection.classList.remove('hidden');

    // Reset button state
    elements.analyzeBtn.querySelector('.btn-text').classList.remove('hidden');
    elements.analyzeBtn.querySelector('.btn-loader').classList.add('hidden');

    // Get overall result (handle both single analysis and full analysis)
    const overallResult = result.overall_result || result;
    const authenticity = overallResult.authenticity_score || result.authenticity_score || 50;
    const confidence = overallResult.confidence || result.confidence || 50;
    const verdict = overallResult.verdict || (authenticity >= 70 ? 'likely_authentic' : authenticity >= 50 ? 'uncertain' : 'likely_fake');
    const isDeepfake = overallResult.is_deepfake || result.is_deepfake || false;

    // Animate score
    animateScore(authenticity);

    // Update confidence
    elements.confidenceFill.style.width = `${confidence}%`;
    elements.confidenceValue.textContent = `${confidence}%`;

    // Update verdict
    updateVerdict(verdict, authenticity);

    // Update details
    displayDetails(result);

    // Update indicators
    displayIndicators(result.indicators || overallResult.indicators || []);

    // Update tips
    displayTips(result.protection_tips || []);

    // Scroll to results
    elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Animate score value and ring
 */
function animateScore(targetScore) {
    const duration = 1500;
    const startTime = performance.now();
    const circumference = 339.292; // 2 * PI * 54

    function animate(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function
        const easeOutCubic = 1 - Math.pow(1 - progress, 3);

        const currentScore = Math.round(targetScore * easeOutCubic);
        elements.scoreValue.textContent = currentScore;

        // Update ring
        const offset = circumference - (circumference * (targetScore / 100) * easeOutCubic);
        elements.scoreRing.style.strokeDashoffset = offset;

        // Update color based on score
        if (currentScore >= 70) {
            elements.scoreValue.style.color = '#10B981';
        } else if (currentScore >= 50) {
            elements.scoreValue.style.color = '#F59E0B';
        } else {
            elements.scoreValue.style.color = '#EF4444';
        }

        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }

    requestAnimationFrame(animate);
}

/**
 * Update verdict display
 */
function updateVerdict(verdict, score) {
    elements.verdictBadge.className = 'verdict-badge';

    switch (verdict) {
        case 'likely_authentic':
            elements.verdictBadge.classList.add('authentic');
            elements.verdictIcon.textContent = '✅';
            elements.verdictText.textContent = 'Likely Authentic';
            elements.scoreDescription.textContent = 'This content appears to be genuine. No significant manipulation indicators were detected.';
            break;
        case 'uncertain':
            elements.verdictBadge.classList.add('uncertain');
            elements.verdictIcon.textContent = '⚠️';
            elements.verdictText.textContent = 'Uncertain - Review Recommended';
            elements.scoreDescription.textContent = 'This content shows some inconsistencies. We recommend additional verification before trusting.';
            break;
        case 'likely_fake':
        default:
            elements.verdictBadge.classList.add('fake');
            elements.verdictIcon.textContent = '🚨';
            elements.verdictText.textContent = 'Likely Deepfake';
            elements.scoreDescription.textContent = 'This content shows signs of manipulation. Exercise caution and do not share without verification.';
            break;
    }
}

/**
 * Display detailed analysis results
 */
function displayDetails(result) {
    elements.detailsGrid.innerHTML = '';

    // Collect all details from various analysis types
    const details = [];

    // Video details
    if (result.details?.video?.details) {
        const vd = result.details.video.details;
        details.push({ label: 'Visual Artifacts', value: 100 - (vd.artifact_score || 50) });
        details.push({ label: 'Color Consistency', value: vd.color_consistency || 50 });
        details.push({ label: 'Noise Analysis', value: vd.noise_analysis || 50 });
        details.push({ label: 'Temporal Consistency', value: vd.temporal_consistency || 50 });
    }

    // Audio details
    if (result.details?.audio?.details) {
        const ad = result.details.audio.details;
        details.push({ label: 'Voice Naturalness', value: ad.voice_naturalness || 50 });
        details.push({ label: 'Rhythm Pattern', value: ad.rhythm_naturalness || 50 });
        details.push({ label: 'Spectral Analysis', value: 100 - (ad.spectral_consistency || 50) });
    }

    // Face landmark details
    if (result.details?.face_landmarks?.details) {
        const fd = result.details.face_landmarks.details;
        details.push({ label: 'Blink Naturalness', value: fd.blink_naturalness || 50 });
        details.push({ label: 'Lip Sync', value: fd.lip_sync_naturalness || 50 });
        details.push({ label: 'Facial Symmetry', value: fd.facial_symmetry || 50 });
        details.push({ label: 'Micro-expressions', value: fd.micro_expression_naturalness || 50 });
    }

    // Single analysis mode details
    if (result.details && !result.overall_result) {
        Object.entries(result.details).forEach(([key, value]) => {
            if (typeof value === 'number') {
                const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                details.push({ label, value });
            }
        });
    }

    // Render details
    if (details.length === 0) {
        details.push({ label: 'Overall Health', value: result.authenticity_score || 50 });
    }

    details.forEach(detail => {
        const item = document.createElement('div');
        item.className = 'detail-item';

        const fillClass = detail.value >= 70 ? 'good' : detail.value >= 50 ? 'warning' : 'bad';

        item.innerHTML = `
            <span class="detail-label">${detail.label}</span>
            <div class="detail-bar">
                <div class="detail-fill ${fillClass}" style="width: ${detail.value}%"></div>
            </div>
            <span class="detail-value">${Math.round(detail.value)}%</span>
        `;

        elements.detailsGrid.appendChild(item);
    });
}

/**
 * Display detection indicators
 */
function displayIndicators(indicators) {
    elements.indicatorsList.innerHTML = '';

    if (indicators.length === 0) {
        indicators = ['Analysis complete - review the scores above for details.'];
    }

    indicators.forEach(indicator => {
        const li = document.createElement('li');
        li.className = 'indicator-item';

        // Determine icon based on content
        let icon = '📌';
        if (indicator.toLowerCase().includes('no ') || indicator.toLowerCase().includes('natural') || indicator.toLowerCase().includes('authentic')) {
            icon = '✅';
        } else if (indicator.toLowerCase().includes('detected') || indicator.toLowerCase().includes('found') || indicator.toLowerCase().includes('unusual')) {
            icon = '⚠️';
        }

        li.innerHTML = `
            <span class="indicator-icon">${icon}</span>
            <span class="indicator-text">${indicator}</span>
        `;

        elements.indicatorsList.appendChild(li);
    });
}

/**
 * Display protection tips
 */
function displayTips(tips) {
    elements.tipsList.innerHTML = '';

    if (tips.length === 0) {
        tips = [
            "Always verify content from multiple sources",
            "Be skeptical of emotionally provocative content",
            "Check the original source of any media"
        ];
    }

    tips.slice(0, 5).forEach(tip => {
        const li = document.createElement('li');
        li.className = 'tip-item';
        li.textContent = tip.replace(/^[🚨⚠️✅🔍📢🛡️👥📋🤔📱🔄📚👀]\s*/, '');
        elements.tipsList.appendChild(li);
    });
}

/**
 * Reset to initial state for new analysis
 */
function resetToInitialState() {
    state.selectedFile = null;
    state.isAnalyzing = false;
    elements.fileInput.value = '';

    // Reset upload zone
    document.querySelector('.upload-content').style.display = 'block';
    elements.uploadPreview.hidden = true;

    // Reset buttons
    elements.analyzeBtn.disabled = true;
    elements.analyzeBtn.querySelector('.btn-text').classList.remove('hidden');
    elements.analyzeBtn.querySelector('.btn-loader').classList.add('hidden');

    // Hide results and progress
    elements.resultsSection.classList.add('hidden');
    elements.analysisProgress.classList.add('hidden');

    // Reset progress
    updateProgress(0, 1);

    // Scroll to upload section
    document.getElementById('detect').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Reset analysis UI after error
 */
function resetAnalysisUI() {
    elements.analyzeBtn.querySelector('.btn-text').classList.remove('hidden');
    elements.analyzeBtn.querySelector('.btn-loader').classList.add('hidden');
    elements.analyzeBtn.disabled = false;
    elements.analysisProgress.classList.add('hidden');
    updateProgress(0, 1);
}

/**
 * Show error message
 */
function showError(message) {
    // Create error toast
    const toast = document.createElement('div');
    toast.className = 'error-toast';
    toast.innerHTML = `
        <span class="toast-icon">⚠️</span>
        <span class="toast-message">${message}</span>
    `;

    // Add styles if not exists
    if (!document.querySelector('#toast-styles')) {
        const style = document.createElement('style');
        style.id = 'toast-styles';
        style.textContent = `
            .error-toast {
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(239, 68, 68, 0.95);
                color: white;
                padding: 16px 24px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                gap: 12px;
                font-weight: 500;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
                z-index: 10000;
                animation: slideUp 0.3s ease;
            }
            @keyframes slideUp {
                from { transform: translateX(-50%) translateY(100%); opacity: 0; }
                to { transform: translateX(-50%) translateY(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(toast);

    // Remove after delay
    setTimeout(() => {
        toast.style.animation = 'slideUp 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

/**
 * Format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Sleep utility
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Demo mode - for testing without backend
 */
function enableDemoMode() {
    CONFIG.API_BASE_URL = '';

    // Mock fetch
    window.originalFetch = window.fetch;
    window.fetch = async (url, options) => {
        await sleep(2000); // Simulate network delay

        // Generate mock results
        const mockResult = {
            success: true,
            filename: state.selectedFile?.name || 'test.mp4',
            timestamp: new Date().toISOString(),
            analyses_performed: ['video', 'audio', 'face_landmarks'],
            overall_result: {
                authenticity_score: Math.floor(Math.random() * 40) + 30,
                confidence: Math.floor(Math.random() * 20) + 70,
                verdict: Math.random() > 0.5 ? 'likely_fake' : 'uncertain',
                is_deepfake: Math.random() > 0.4
            },
            details: {
                video: {
                    success: true,
                    details: {
                        artifact_score: Math.floor(Math.random() * 40) + 30,
                        color_consistency: Math.floor(Math.random() * 30) + 50,
                        noise_analysis: Math.floor(Math.random() * 30) + 40,
                        temporal_consistency: Math.floor(Math.random() * 30) + 50
                    }
                },
                face_landmarks: {
                    success: true,
                    details: {
                        blink_naturalness: Math.floor(Math.random() * 40) + 40,
                        lip_sync_naturalness: Math.floor(Math.random() * 30) + 50,
                        facial_symmetry: Math.floor(Math.random() * 20) + 60,
                        micro_expression_naturalness: Math.floor(Math.random() * 30) + 45
                    }
                }
            },
            indicators: [
                'Compression artifacts detected around face region',
                'Unusual blink pattern frequency detected',
                'Minor lip-sync irregularities found'
            ],
            protection_tips: [
                '🚨 This content shows signs of manipulation. Do not share without verification.',
                '🔍 Cross-reference with official sources before trusting this media.',
                '📢 Report suspicious content to the platform where you found it.'
            ]
        };

        return {
            ok: true,
            json: async () => mockResult
        };
    };

    console.log('🎮 Demo mode enabled - results are simulated');
}

// Uncomment to enable demo mode for testing:
// enableDemoMode();
