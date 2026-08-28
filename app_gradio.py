import os
import glob
import time
import cv2
import numpy as np
from PIL import Image
import torch
from ultralytics import YOLO
import gradio as gr

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "weights", "best.pt")
SAMPLES_DIR = os.path.join(BASE_DIR, "static", "samples")

# Fallback model discovery
if not os.path.exists(MODEL_PATH):
    candidates = [
        os.path.join(BASE_DIR, "best.pt"),
        os.path.join(BASE_DIR, "runs", "detect", "GymAI_App", "run_01-2", "weights", "best.pt"),
        "best.pt",
        "yolov8s.pt"
    ]
    for c in candidates:
        if os.path.exists(c):
            MODEL_PATH = c
            break

# Detect Device
DEVICE = 0 if torch.cuda.is_available() else "cpu"
print(f"🚀 [Gym AI Gradio] Loading Model: {MODEL_PATH} on Device: {DEVICE}")

# Load YOLO Model
try:
    model = YOLO(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    model = None

# Sample Images list
sample_images = []
if os.path.exists(SAMPLES_DIR):
    sample_images = sorted(glob.glob(os.path.join(SAMPLES_DIR, "*.jpg")))


def detect_gym_equipment(input_img, conf_threshold=0.25, iou_threshold=0.45):
    """
    Run YOLO detection on the input image or webcam snapshot.
    Returns:
        - Annotated PIL Image
        - Markdown summary of detections and inference latency
    """
    if input_img is None:
        return None, "⚠️ Vui lòng tải ảnh lên hoặc chụp từ camera."

    if model is None:
        return input_img, "❌ Lỗi: Không tìm thấy file trọng số mô hình `weights/best.pt`."

    start_time = time.perf_counter()

    # Convert PIL to BGR OpenCV format
    if isinstance(input_img, np.ndarray):
        img_bgr = cv2.cvtColor(input_img, cv2.COLOR_RGB2BGR)
    else:
        img_bgr = cv2.cvtColor(np.array(input_img), cv2.COLOR_RGB2BGR)

    # Scale if too large on CPU
    h, w = img_bgr.shape[:2]
    if DEVICE == "cpu" and max(h, w) > 960:
        scale = 960 / max(h, w)
        img_bgr = cv2.resize(img_bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    # Run YOLO Prediction
    with torch.no_grad():
        results = model.predict(
            source=img_bgr,
            conf=conf_threshold,
            iou=iou_threshold,
            imgsz=640 if DEVICE == 0 else 512,
            device=DEVICE,
            verbose=False
        )

    latency_ms = round((time.perf_counter() - start_time) * 1000, 1)

    result = results[0]
    boxes = result.boxes

    # Draw colorful bounding boxes
    annotated_bgr = img_bgr.copy()
    detections_summary = []

    COLORS = [
        (0, 255, 127),   # Spring Green
        (255, 105, 180), # Hot Pink
        (30, 144, 255),  # Dodger Blue
        (255, 215, 0),   # Gold
        (138, 43, 226),  # Blue Violet
        (0, 255, 255),   # Cyan
        (255, 69, 0),    # Orange Red
        (50, 205, 50),   # Lime Green
    ]

    if boxes is not None and len(boxes) > 0:
        for idx, box in enumerate(boxes):
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            class_name = model.names.get(cls_id, f"Class {cls_id}")
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            color = COLORS[cls_id % len(COLORS)]

            # Draw box
            cv2.rectangle(annotated_bgr, (x1, y1), (x2, y2), color, 3)

            # Draw label banner
            label = f"{class_name} {conf * 100:.1f}%"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(annotated_bgr, (x1, max(0, y1 - th - 10)), (x1 + tw + 10, y1), color, -1)
            cv2.putText(annotated_bgr, label, (x1 + 5, max(th + 2, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

            detections_summary.append({
                "STT": idx + 1,
                "Thiết bị": class_name,
                "Độ tin cậy": f"{conf * 100:.1f}%"
            })

    # Convert back to RGB for Gradio
    annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)
    annotated_pil = Image.fromarray(annotated_rgb)

    # Format Markdown Report
    count = len(detections_summary)
    report_md = f"""### 📊 Kết Quả Nhận Diện AI
- **⚡ Thời gian suy luận:** `{latency_ms} ms`
- **🏋️‍♂️ Số thiết bị tìm thấy:** `{count}` thiết bị
- **💻 Phần cứng:** `{GPU_NAME if 'GPU_NAME' in globals() else DEVICE}`

| # | Tên thiết bị (Gym Equipment) | Độ tin cậy (Confidence) |
| :-: | :--- | :---: |
"""
    if count == 0:
        report_md += "| - | *Không tìm thấy thiết bị nào (Hãy thử giảm Confidence)* | - |\n"
    else:
        for item in detections_summary:
            report_md += f"| **{item['STT']}** | `{item['Thiết bị']}` | **{item['Độ tin cậy']}** |\n"

    return annotated_pil, report_md


# Custom Cyberpunk Theme CSS
custom_css = """
body {
    background-color: #0b0f19;
    color: #e2e8f0;
}
.gradio-container {
    max-width: 1100px !important;
    margin: auto !important;
    font-family: 'Inter', system-ui, sans-serif !important;
}
.header-title {
    text-align: center;
    background: linear-gradient(135deg, #00ff7f 0%, #00f2fe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.3rem !important;
    font-weight: 800 !important;
    margin-bottom: 6px;
}
.header-desc {
    text-align: center;
    color: #94a3b8;
    font-size: 1.05rem;
    margin-bottom: 24px;
}
"""

# Build Gradio Interface
with gr.Blocks(css=custom_css, title="Gym AI - Equipment Detector") as demo:
    gr.HTML("""
        <div style="text-align: center; padding: 20px 0 10px;">
            <h1 class="header-title">🏋️‍♂️ GYM AI VISION</h1>
            <p class="header-desc">Hệ thống AI nhận diện <b>69 loại thiết bị & máy tập Gym</b> theo thời gian thực (YOLOv8s - mAP50 82.8%)</p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=5):
            input_image = gr.Image(
                label="📷 Tải ảnh lên hoặc Chụp từ Camera",
                type="pil",
                sources=["upload", "webcam", "clipboard"]
            )
            
            with gr.Accordion("⚙️ Tùy chỉnh tham số AI", open=False):
                conf_slider = gr.Slider(
                    minimum=0.1, maximum=0.95, value=0.25, step=0.05,
                    label="Độ tin cậy tối thiểu (Confidence Threshold)"
                )
                iou_slider = gr.Slider(
                    minimum=0.1, maximum=0.9, value=0.45, step=0.05,
                    label="Ngưỡng triệt tiêu trùng lặp (IoU NMS)"
                )

            detect_btn = gr.Button("⚡ Nhận Diện Thiết Bị Ngay", variant="primary", size="lg")

            if sample_images:
                gr.Examples(
                    examples=[[img] for img in sample_images[:6]],
                    inputs=[input_image],
                    label="💡 Click vào ảnh mẫu bên dưới để test ngay:"
                )

        with gr.Column(scale=5):
            output_image = gr.Image(label="🎯 Ảnh kết quả với Bounding Box", type="pil")
            output_report = gr.Markdown("### 📊 Kết Quả Nhận Diện Sẽ Hiển Thị Ở Đây")

    # Wire event listener
    detect_btn.click(
        fn=detect_gym_equipment,
        inputs=[input_image, conf_slider, iou_slider],
        outputs=[output_image, output_report]
    )

    input_image.change(
        fn=detect_gym_equipment,
        inputs=[input_image, conf_slider, iou_slider],
        outputs=[output_image, output_report]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
