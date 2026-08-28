/**
 * GYM AI - REALTIME DETECTION APPLICATION JAVASCRIPT
 * Handles Live Webcam Stream, Image Drag & Drop, Fast Inference & Interactive UI
 */

// Global Application State
const state = {
    activeTab: 'webcam',
    isStreaming: false,
    mediaStream: null,
    facingMode: 'user', // 'user' (front) or 'environment' (back)
    confidence: 0.25,
    iou: 0.45,
    isProcessingFrame: false,
    lastFrameTime: performance.now(),
    frameCount: 0,
    fps: 0,
    fpsInterval: null,
    selectedImageBlob: null
};

// DOM Elements Cache
const DOM = {
    tabWebcamBtn: document.getElementById('tabWebcamBtn'),
    tabUploadBtn: document.getElementById('tabUploadBtn'),
    webcamView: document.getElementById('webcamView'),
    uploadView: document.getElementById('uploadView'),
    webcam: document.getElementById('webcamElement'),
    canvas: document.getElementById('detectionCanvas'),
    cameraStandby: document.getElementById('cameraStandby'),
    floatingHud: document.getElementById('floatingHud'),
    scannerBar: document.getElementById('scannerBar'),
    toggleCamBtn: document.getElementById('toggleCamBtn'),
    toggleCamText: document.getElementById('toggleCamText'),
    flipCamBtn: document.getElementById('flipCamBtn'),
    camStatusDot: document.getElementById('camStatusDot'),
    camStatusText: document.getElementById('camStatusText'),
    confSlider: document.getElementById('confSlider'),
    confValue: document.getElementById('confValue'),
    iouSlider: document.getElementById('iouSlider'),
    iouValue: document.getElementById('iouValue'),
    statLatency: document.getElementById('statLatency'),
    statCount: document.getElementById('statCount'),
    statFps: document.getElementById('statFps'),
    hudFps: document.getElementById('hudFps'),
    hudLatency: document.getElementById('hudLatency'),
    hudCount: document.getElementById('hudCount'),
    detectionsList: document.getElementById('detectionsList'),
    detectionBadgeCount: document.getElementById('detectionBadgeCount'),
    dropzone: document.getElementById('dropzone'),
    fileInput: document.getElementById('fileInput'),
    imageResultWrapper: document.getElementById('imageResultWrapper'),
    resultImage: document.getElementById('resultImage'),
    downloadBtn: document.getElementById('downloadBtn'),
    sampleGrid: document.getElementById('sampleGrid'),
    toast: document.getElementById('toast'),
    modelNameDisplay: document.getElementById('modelNameDisplay'),
    aiLoadingOverlay: document.getElementById('aiLoadingOverlay'),
    progressBarFill: document.getElementById('progressBarFill'),
    progressStage: document.getElementById('progressStage'),
    progressPercent: document.getElementById('progressPercent'),
    loadingTitle: document.getElementById('loadingTitle'),
    loadingSubtitle: document.getElementById('loadingSubtitle')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    fetchModelInfo();
    fetchSampleImages();
    setupFpsCalculator();
});

// Toast notification helper
function showToast(message, type = 'success') {
    if (!DOM.toast) return;
    DOM.toast.innerHTML = `<i class="fa-solid ${type === 'success' ? 'fa-circle-check' : 'fa-triangle-exclamation'}"></i> ${message}`;
    DOM.toast.className = `toast show ${type}`;
    setTimeout(() => {
        DOM.toast.className = 'toast';
    }, 3500);
}

// Tab Switching
function switchTab(tab) {
    state.activeTab = tab;
    
    if (tab === 'webcam') {
        DOM.tabWebcamBtn.classList.add('active');
        DOM.tabUploadBtn.classList.remove('active');
        DOM.webcamView.classList.add('active');
        DOM.uploadView.classList.remove('active');
    } else {
        DOM.tabWebcamBtn.classList.remove('active');
        DOM.tabUploadBtn.classList.add('active');
        DOM.webcamView.classList.remove('active');
        DOM.uploadView.classList.add('active');
        
        // Pause camera if running when switching to upload
        if (state.isStreaming) {
            stopWebcam();
            showToast("Đã tạm dừng camera khi chuyển sang tab tải ảnh", "info");
        }
    }
}

// Fetch Model Information
async function fetchModelInfo() {
    try {
        const response = await fetch('/api/model-info');
        const data = await response.json();
        if (data.status === 'active') {
            if (DOM.modelNameDisplay) {
                DOM.modelNameDisplay.textContent = `${data.model_name} (${data.classes_count} lớp)`;
            }
        }
    } catch (e) {
        console.warn("Could not fetch model info:", e);
    }
}

// ============================================================
// WEBCAM & REAL-TIME STREAMING
// ============================================================

async function startWebcam() {
    try {
        DOM.camStatusText.textContent = "Đang kết nối camera...";
        
        const constraints = {
            video: {
                facingMode: state.facingMode,
                width: { ideal: 1280 },
                height: { ideal: 720 }
            },
            audio: false
        };

        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        state.mediaStream = stream;
        DOM.webcam.srcObject = stream;

        await new Promise((resolve) => {
            DOM.webcam.onloadedmetadata = () => {
                DOM.webcam.play();
                resolve();
            };
        });

        // Setup Canvas Dimensions
        DOM.canvas.width = DOM.webcam.videoWidth || 1280;
        DOM.canvas.height = DOM.webcam.videoHeight || 720;

        state.isStreaming = true;
        DOM.cameraStandby.style.display = 'none';
        DOM.floatingHud.style.display = 'flex';
        DOM.scannerBar.style.display = 'block';
        DOM.camStatusDot.classList.add('active');
        DOM.camStatusText.textContent = "Camera đang hoạt động";
        DOM.toggleCamText.textContent = "Dừng Camera";
        DOM.toggleCamBtn.className = "btn btn-secondary";

        showToast("Đã kích hoạt camera thành công!", "success");

        // Start processing loop
        processWebcamLoop();

    } catch (err) {
        console.error("Webcam Error:", err);
        DOM.camStatusText.textContent = "Lỗi camera";
        showToast(`Không thể mở camera: ${err.message || 'Thiết bị không hỗ trợ'}`, "error");
    }
}

function stopWebcam() {
    if (state.mediaStream) {
        state.mediaStream.getTracks().forEach(track => track.stop());
        state.mediaStream = null;
    }
    
    state.isStreaming = false;
    DOM.webcam.srcObject = null;
    
    // Reset Canvas
    const ctx = DOM.canvas.getContext('2d');
    ctx.clearRect(0, 0, DOM.canvas.width, DOM.canvas.height);

    DOM.cameraStandby.style.display = 'flex';
    DOM.floatingHud.style.display = 'none';
    DOM.scannerBar.style.display = 'none';
    DOM.camStatusDot.classList.remove('active');
    DOM.camStatusText.textContent = "Sẵn sàng";
    DOM.toggleCamText.textContent = "Bật Camera";
    DOM.toggleCamBtn.className = "btn btn-primary";

    // Clear stats
    updateStats(0, 0, 0);
    renderDetectionsList([]);
}

function toggleWebcam() {
    if (state.isStreaming) {
        stopWebcam();
    } else {
        startWebcam();
    }
}

function flipCamera() {
    state.facingMode = state.facingMode === 'user' ? 'environment' : 'user';
    if (state.isStreaming) {
        stopWebcam();
        startWebcam();
    }
}

// Real-time Frame Loop
async function processWebcamLoop() {
    if (!state.isStreaming) return;

    if (!state.isProcessingFrame && DOM.webcam.readyState === DOM.webcam.HAVE_ENOUGH_DATA) {
        state.isProcessingFrame = true;
        
        try {
            // Draw current video frame to an offscreen canvas
            const offCanvas = document.createElement('canvas');
            offCanvas.width = 640;
            offCanvas.height = 480;
            const offCtx = offCanvas.getContext('2d');
            offCtx.drawImage(DOM.webcam, 0, 0, offCanvas.width, offCanvas.height);
            
            const frameBase64 = offCanvas.toDataURL('image/jpeg', 0.82);

            const startTime = performance.now();
            const response = await fetch('/api/detect-frame', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    image: frameBase64,
                    confidence: state.confidence,
                    iou: state.iou
                })
            });

            const data = await response.json();
            const inferenceTime = Math.round(performance.now() - startTime);

            if (data.success && state.isStreaming) {
                // Render returned annotated image on the visible canvas
                const img = new Image();
                img.onload = () => {
                    const ctx = DOM.canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, DOM.canvas.width, DOM.canvas.height);
                };
                img.src = data.annotated_image;

                // Update Stats & List
                updateStats(data.inference_time_ms || inferenceTime, data.count, state.fps);
                renderDetectionsList(data.detections);
                state.frameCount++;
            }

        } catch (err) {
            console.error("Frame inference error:", err);
        } finally {
            state.isProcessingFrame = false;
        }
    }

    // Schedule next frame with requestAnimationFrame
    if (state.isStreaming) {
        requestAnimationFrame(processWebcamLoop);
    }
}

function setupFpsCalculator() {
    setInterval(() => {
        state.fps = state.frameCount;
        state.frameCount = 0;
        if (state.isStreaming) {
            DOM.statFps.innerHTML = `${state.fps} <small>FPS</small>`;
            DOM.hudFps.textContent = state.fps;
        }
    }, 1000);
}

function takeSnapshot() {
    if (!state.isStreaming) {
        showToast("Vui lòng bật camera để chụp frame!", "error");
        return;
    }

    const dataUrl = DOM.canvas.toDataURL('image/jpeg', 0.95);
    const link = document.createElement('a');
    link.download = `gym_snapshot_${Date.now()}.jpg`;
    link.href = dataUrl;
    link.click();
    showToast("Đã lưu ảnh chụp màn hình!", "success");
}

// ============================================================
// IMAGE UPLOAD & DROPZONE
// ============================================================

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    DOM.dropzone.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    DOM.dropzone.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    DOM.dropzone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
        processUploadedFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files && files.length > 0) {
        processUploadedFile(files[0]);
    }
}

async function processUploadedFile(file) {
    if (!file.type.startsWith('image/')) {
        showToast("Vui lòng chọn file hình ảnh (JPG, PNG, WEBP)!", "error");
        return;
    }

    state.selectedImageBlob = file;
    await runImageInference(file);
}

// ============================================================
// AI LOADING OVERLAY & PROGRESS BAR ANIMATOR
// ============================================================

let progressInterval = null;

function startAiLoadingAnimation() {
    if (!DOM.aiLoadingOverlay) return;
    
    DOM.aiLoadingOverlay.style.display = 'flex';
    DOM.progressBarFill.style.width = '5%';
    DOM.progressPercent.textContent = '5%';
    DOM.progressStage.textContent = 'Đang nạp ảnh vào AI...';

    let currentProgress = 5;
    const stages = [
        { threshold: 25, text: 'Đang tải ảnh & tiền xử lý tensor...' },
        { threshold: 50, text: 'Đang quét nhận diện 69 thiết bị Gym...' },
        { threshold: 75, text: 'Đang tính toán Bounding Box & IoU...' },
        { threshold: 92, text: 'Đang kết xuất khung định vị thiết bị...' },
        { threshold: 98, text: 'Đang tối ưu ảnh trả về client...' }
    ];

    if (progressInterval) clearInterval(progressInterval);

    progressInterval = setInterval(() => {
        if (currentProgress < 96) {
            const diff = 97 - currentProgress;
            const step = Math.max(0.5, diff * 0.08);
            currentProgress = Math.min(96, Math.round((currentProgress + step) * 10) / 10);
            
            DOM.progressBarFill.style.width = `${Math.floor(currentProgress)}%`;
            DOM.progressPercent.textContent = `${Math.floor(currentProgress)}%`;

            for (const stage of stages) {
                if (currentProgress <= stage.threshold) {
                    DOM.progressStage.textContent = stage.text;
                    break;
                }
            }
        }
    }, 150);
}

function completeAiLoadingAnimation(onComplete) {
    if (progressInterval) clearInterval(progressInterval);
    
    if (DOM.progressBarFill) {
        DOM.progressBarFill.style.width = '100%';
        DOM.progressPercent.textContent = '100%';
        DOM.progressStage.textContent = '✅ Hoàn tất nhận diện!';
    }

    setTimeout(() => {
        if (DOM.aiLoadingOverlay) {
            DOM.aiLoadingOverlay.style.display = 'none';
        }
        if (typeof onComplete === 'function') onComplete();
    }, 320);
}

function hideAiLoadingAnimation() {
    if (progressInterval) clearInterval(progressInterval);
    if (DOM.aiLoadingOverlay) {
        DOM.aiLoadingOverlay.style.display = 'none';
    }
}

async function runImageInference(fileOrBlob) {
    const formData = new FormData();
    formData.append('file', fileOrBlob, 'test_image.jpg');
    formData.append('confidence', state.confidence);
    formData.append('iou', state.iou);

    DOM.dropzone.style.display = 'none';
    DOM.imageResultWrapper.style.display = 'flex';
    
    // Show instant preview of the uploaded image immediately
    try {
        DOM.resultImage.src = URL.createObjectURL(fileOrBlob);
    } catch (e) {
        // Fallback
    }

    // Start progress bar animation
    startAiLoadingAnimation();

    try {
        const response = await fetch('/api/detect-image', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            completeAiLoadingAnimation(() => {
                DOM.resultImage.src = data.annotated_image;
                DOM.downloadBtn.href = data.annotated_image;
                
                updateStats(data.inference_time_ms, data.count, 0);
                renderDetectionsList(data.detections);
                showToast(`Phát hiện ${data.count} thiết bị trong ${data.inference_time_ms}ms!`, "success");
            });
        } else {
            hideAiLoadingAnimation();
            showToast(`Lỗi nhận diện: ${data.error || 'Thử lại sau'}`, "error");
        }

    } catch (err) {
        console.error("Image inference error:", err);
        hideAiLoadingAnimation();
        showToast("Lỗi kết nối máy chủ nhận diện!", "error");
    }
}

function clearUpload() {
    state.selectedImageBlob = null;
    DOM.dropzone.style.display = 'flex';
    DOM.imageResultWrapper.style.display = 'none';
    DOM.fileInput.value = '';
    updateStats(0, 0, 0);
    renderDetectionsList([]);
}

// ============================================================
// SAMPLE DATASET IMAGES
// ============================================================

async function fetchSampleImages() {
    try {
        const response = await fetch('/api/sample-images');
        const data = await response.json();
        
        if (data.samples && data.samples.length > 0) {
            DOM.sampleGrid.innerHTML = '';
            data.samples.slice(0, 8).forEach((sampleName, index) => {
                const card = document.createElement('div');
                card.className = 'sample-card';
                card.title = `Ảnh mẫu test #${index + 1}`;
                card.onclick = () => loadSampleImage(sampleName);

                const img = document.createElement('img');
                img.src = `/api/sample-image-file/${sampleName}`;
                img.alt = `Sample ${index + 1}`;
                img.loading = "lazy";

                card.appendChild(img);
                DOM.sampleGrid.appendChild(card);
            });
        } else {
            DOM.sampleGrid.innerHTML = '<small class="text-dim">Không tìm thấy ảnh mẫu</small>';
        }
    } catch (e) {
        console.warn("Could not load sample images:", e);
    }
}

async function loadSampleImage(filename) {
    try {
        showToast("Đang nạp ảnh mẫu và nhận diện...", "info");
        const response = await fetch(`/api/sample-image-file/${filename}`);
        const blob = await response.blob();
        state.selectedImageBlob = blob;
        await runImageInference(blob);
    } catch (e) {
        showToast("Không thể nạp ảnh mẫu!", "error");
    }
}

// ============================================================
// CONTROLS & UI UPDATES
// ============================================================

function updateConfidence(val) {
    state.confidence = parseFloat(val);
    DOM.confValue.textContent = `${Math.round(state.confidence * 100)}%`;
    
    // If in upload tab and an image is active, re-run with new threshold
    if (state.activeTab === 'upload' && state.selectedImageBlob) {
        runImageInference(state.selectedImageBlob);
    }
}

function updateIoU(val) {
    state.iou = parseFloat(val);
    DOM.iouValue.textContent = `${Math.round(state.iou * 100)}%`;
    
    if (state.activeTab === 'upload' && state.selectedImageBlob) {
        runImageInference(state.selectedImageBlob);
    }
}

function updateStats(latency, count, fps) {
    if (DOM.statLatency) DOM.statLatency.innerHTML = `${latency} <small>ms</small>`;
    if (DOM.statCount) DOM.statCount.textContent = count;
    if (DOM.statFps && fps > 0) DOM.statFps.innerHTML = `${fps} <small>FPS</small>`;

    if (DOM.hudLatency) DOM.hudLatency.textContent = `${latency}ms`;
    if (DOM.hudCount) DOM.hudCount.textContent = count;
}

function renderDetectionsList(detections) {
    if (!DOM.detectionsList) return;

    if (!detections || detections.length === 0) {
        DOM.detectionBadgeCount.textContent = '0 mục';
        DOM.detectionsList.innerHTML = `
            <div class="empty-detections">
                <i class="fa-solid fa-layer-group"></i>
                <p>Chưa có thiết bị nào được phát hiện</p>
                <small>Đưa dụng cụ tập vào camera hoặc tải ảnh lên để bắt đầu</small>
            </div>
        `;
        return;
    }

    DOM.detectionBadgeCount.textContent = `${detections.length} mục`;
    
    let html = '';
    detections.forEach(det => {
        html += `
            <div class="detection-card" style="border-left-color: ${det.color || '#00ff7f'};">
                <div class="det-info">
                    <span class="det-name">${det.class_name}</span>
                    <span class="det-id">Box: [${det.box.join(', ')}]</span>
                </div>
                <div class="det-score">
                    <span class="score-text">${det.confidence_percent}%</span>
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width: ${det.confidence_percent}%;"></div>
                    </div>
                </div>
            </div>
        `;
    });

    DOM.detectionsList.innerHTML = html;
}
