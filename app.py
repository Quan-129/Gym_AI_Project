import os
import io
import time
import base64
import glob
from typing import List, Optional
import cv2
import numpy as np
from PIL import Image
import torch
from ultralytics import YOLO
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI App
app = FastAPI(
    title="Gym AI - Equipment Detector",
    description="Real-time 69 Gym Equipment Detection using YOLOv8 & PyTorch GPU",
    version="1.0.0"
)

# Enable CORS for easy cross-origin testing if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEST_IMAGES_DIR = os.path.join(BASE_DIR, "Gym-Dataset-2", "test", "images")

# Ensure directories exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "js"), exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Find Best Model Weight
MODEL_CANDIDATES = [
    os.path.join(BASE_DIR, "weights", "best.pt"),
    os.path.join(BASE_DIR, "runs", "detect", "GymAI_App", "run_01-2", "weights", "best.pt"),
    os.path.join(BASE_DIR, "runs", "detect", "GymAI_App", "run_01", "weights", "best.pt"),
    os.path.join(BASE_DIR, "best.pt"),
    os.path.join(BASE_DIR, "yolov8s.pt"),
]

MODEL_PATH = None
for candidate in MODEL_CANDIDATES:
    if os.path.exists(candidate):
        MODEL_PATH = candidate
        break

if not MODEL_PATH:
    MODEL_PATH = "yolov8s.pt"

# Detect GPU
DEVICE = 0 if torch.cuda.is_available() else "cpu"
GPU_NAME = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"

print(f"🚀 [Gym AI] Loading model: {MODEL_PATH}")
print(f"⚡ [Gym AI] Device: {DEVICE} ({GPU_NAME})")

try:
    model = YOLO(MODEL_PATH)
    # Warmup inference
    dummy = np.zeros((640, 640, 3), dtype=np.uint8)
    model.predict(dummy, device=DEVICE, verbose=False)
    print("✅ [Gym AI] Model loaded & warmed up successfully!")
except Exception as e:
    print(f"⚠️ [Gym AI] Error loading model {MODEL_PATH}: {e}")
    model = None


def process_detections(results, orig_img_bgr, conf_threshold: float = 0.25):
    """Format YOLO results and generate annotated base64 image."""
    detections = []
    annotated_bgr = orig_img_bgr.copy()

    # Distinct vibrant color palette for visual wow factor
    COLORS = [
        (0, 255, 127),   # Spring Green
        (255, 105, 180), # Hot Pink
        (30, 144, 255),  # Dodger Blue
        (255, 215, 0),   # Gold
        (138, 43, 226),  # Blue Violet
        (0, 255, 255),   # Cyan
        (255, 69, 0),    # Orange Red
        (50, 205, 50),   # Lime Green
        (255, 20, 147),  # Deep Pink
        (0, 191, 255)    # Deep Sky Blue
    ]

    h, w, _ = orig_img_bgr.shape

    if results and len(results) > 0:
        boxes = results[0].boxes
        if boxes is not None and len(boxes) > 0:
            for i, box in enumerate(boxes):
                score = float(box.conf[0].item())
                if score < conf_threshold:
                    continue

                cls_id = int(box.cls[0].item())
                cls_name = results[0].names.get(cls_id, f"Class {cls_id}")
                xyxy = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = map(int, xyxy)

                # Clamp to image bounds
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)

                color = COLORS[cls_id % len(COLORS)]

                # Draw bounding box with rounded corner effect or sleek glow
                cv2.rectangle(annotated_bgr, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)

                # Draw semi-transparent header tag for label
                label_text = f"{cls_name} {score * 100:.1f}%"
                font = cv2.FONT_HERSHEY_DUPLEX
                font_scale = 0.55
                font_thickness = 1
                (text_w, text_h), baseline = cv2.getTextSize(label_text, font, font_scale, font_thickness)

                # Draw label background
                tag_y1 = max(0, y1 - text_h - 8)
                tag_y2 = y1
                tag_x2 = min(w, x1 + text_w + 10)

                overlay = annotated_bgr.copy()
                cv2.rectangle(overlay, (x1, tag_y1), (tag_x2, tag_y2), color, -1)
                cv2.addWeighted(overlay, 0.85, annotated_bgr, 0.15, 0, annotated_bgr)

                # Draw text in contrasting dark or white
                text_color = (0, 0, 0) if (color[0]*0.299 + color[1]*0.587 + color[2]*0.114) > 150 else (255, 255, 255)
                cv2.putText(annotated_bgr, label_text, (x1 + 5, y1 - 5), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

                detections.append({
                    "id": i + 1,
                    "class_id": cls_id,
                    "class_name": cls_name,
                    "confidence": round(score, 4),
                    "confidence_percent": round(score * 100, 1),
                    "box": [x1, y1, x2, y2],
                    "color": f"rgb({color[2]},{color[1]},{color[0]})"
                })

    # Encode annotated image to JPEG base64
    _, buffer = cv2.imencode('.jpg', annotated_bgr, [cv2.IMWRITE_JPEG_QUALITY, 88])
    base64_img = base64.b64encode(buffer).decode('utf-8')

    return detections, f"data:image/jpeg;base64,{base64_img}"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the main web application page."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "gpu_name": GPU_NAME,
            "is_cuda": torch.cuda.is_available(),
            "model_name": os.path.basename(MODEL_PATH)
        }
    )


@app.get("/api/model-info")
async def get_model_info():
    """Return model architecture and active runtime information."""
    class_names = []
    if model and hasattr(model, 'names'):
        class_names = [model.names[k] for k in sorted(model.names.keys())]

    return {
        "status": "active" if model is not None else "error",
        "model_path": MODEL_PATH,
        "model_name": os.path.basename(MODEL_PATH),
        "device": str(DEVICE),
        "gpu_name": GPU_NAME,
        "cuda_available": torch.cuda.is_available(),
        "classes_count": len(class_names),
        "classes": class_names,
        "training_mAP50": 0.8278, # 82.8% on Run 01-2 Epoch 30
        "precision": 0.8013,
        "recall": 0.7628
    }


@app.post("/api/detect-image")
async def detect_image(
    file: UploadFile = File(...),
    confidence: float = Form(0.25),
    iou: float = Form(0.45)
):
    """Run YOLO equipment detection on an uploaded image file."""
    if not model:
        raise HTTPException(status_code=500, detail="Mô hình AI chưa được nạp.")

    start_time = time.perf_counter()

    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img_bgr is None:
            raise HTTPException(status_code=400, detail="Không thể đọc định dạng ảnh tải lên.")

        # Run inference
        results = model.predict(
            source=img_bgr,
            conf=confidence,
            iou=iou,
            device=DEVICE,
            verbose=False
        )

        inference_time_ms = round((time.perf_counter() - start_time) * 1000, 1)

        detections, annotated_image_url = process_detections(results, img_bgr, conf_threshold=confidence)

        return {
            "success": True,
            "inference_time_ms": inference_time_ms,
            "count": len(detections),
            "detections": detections,
            "annotated_image": annotated_image_url,
            "image_size": {"width": img_bgr.shape[1], "height": img_bgr.shape[0]}
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@app.post("/api/detect-frame")
async def detect_frame(request: Request):
    """Run high-speed detection on a single base64 webcam frame."""
    if not model:
        raise HTTPException(status_code=500, detail="Mô hình AI chưa sẵn sàng.")

    start_time = time.perf_counter()

    try:
        data = await request.json()
        image_data = data.get("image")
        confidence = float(data.get("confidence", 0.25))
        iou = float(data.get("iou", 0.45))

        if not image_data:
            raise HTTPException(status_code=400, detail="Không có dữ liệu frame ảnh.")

        # Strip header if present
        if "base64," in image_data:
            image_data = image_data.split("base64,")[1]

        img_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img_bgr is None:
            raise HTTPException(status_code=400, detail="Giải mã frame ảnh thất bại.")

        results = model.predict(
            source=img_bgr,
            conf=confidence,
            iou=iou,
            device=DEVICE,
            verbose=False
        )

        inference_time_ms = round((time.perf_counter() - start_time) * 1000, 1)
        detections, annotated_image_url = process_detections(results, img_bgr, conf_threshold=confidence)

        return {
            "success": True,
            "inference_time_ms": inference_time_ms,
            "count": len(detections),
            "detections": detections,
            "annotated_image": annotated_image_url
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@app.get("/api/sample-images")
async def get_sample_images():
    """List sample test images available in the dataset for 1-click testing."""
    sample_files = []
    if os.path.exists(TEST_IMAGES_DIR):
        files = glob.glob(os.path.join(TEST_IMAGES_DIR, "*.jpg"))[:12]
        for f in files:
            sample_files.append(os.path.basename(f))

    return {"samples": sample_files}


@app.get("/api/sample-image-file/{filename}")
async def get_sample_image_file(filename: str):
    """Serve a sample image file from the test dataset."""
    file_path = os.path.join(TEST_IMAGES_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File không tồn tại.")
    return FileResponse(file_path, media_type="image/jpeg")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🔥 Starting Gym AI Web App at http://127.0.0.1:{port} ...")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
