# 🏋️‍♂️ Gym AI Project - Intelligent Gym Equipment & Workout Assistant

[![Live Demo](https://img.shields.io/badge/Render-Live%20Demo-46E3B7.svg?style=for-the-badge&logo=render&logoColor=white)](https://gym-ai-project-44yz.onrender.com/)
[![Python Version](https://img.shields.io/badge/Python-3.11.9-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.5.1%2Bcu121-EE4C2C.svg?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Ultralytics YOLOv8](https://img.shields.io/badge/YOLOv8-8.4.130-00FFFF.svg?style=for-the-badge)](https://github.com/ultralytics/ultralytics)
[![Hardware](https://img.shields.io/badge/GPU-RTX%204050%206GB-76B900.svg?style=for-the-badge&logo=nvidia&logoColor=white)](https://www.nvidia.com/)
[![License](https://img.shields.io/badge/Dataset-Roboflow%20CC%20BY%204.0-FF6F00.svg?style=for-the-badge)](https://universe.roboflow.com/akash-edwin-samuel/gym-dataset-zfznf/dataset/2)

> **Gym AI** là dự án thị giác máy tính thông minh (Computer Vision AI) hỗ trợ nhận diện **69 loại thiết bị và dụng cụ phòng gym** theo thời gian thực. Dự án tích hợp Web App tương tác trực quan qua Camera & Tải ảnh, đồng thời xây dựng nền tảng cho việc tự động phân tích tư thế tập luyện (Pose Estimation) và đếm số lần tập (Rep Counting).

🌐 **Trải nghiệm trực tiếp trên Web:** **[https://gym-ai-project-44yz.onrender.com/](https://gym-ai-project-44yz.onrender.com/)**

---

## 📌 Tính năng chính (Key Features)

- [x] **Nhận diện 69 lớp thiết bị Gym:** Nhận diện chính xác máy tập, tạ đơn, tạ đòn, máy kéo cáp, máy chạy bộ, xe đạp tập,... (**mAP50 đạt 82.8%**).
- [x] **Web App Responsive Hiện đại:** 
  - 📷 **Live Camera Stream:** Nhận diện thời gian thực qua webcam laptop/điện thoại, đo FPS và độ trễ AI (Latency ms).
  - 🖼️ **Image Drag & Drop:** Kéo thả tải ảnh lên để test, tích hợp kho ảnh mẫu (Sample Images) test nhanh với 1 click.
  - 🎛️ **Điều khiển linh hoạt:** Tùy chỉnh thanh trượt Confidence Threshold (10% - 95%) và IoU NMS.
- [x] **Hỗ trợ đa định dạng mô hình:** Cung cấp cả trọng số **PyTorch** (`weights/best.pt`) và **ONNX** (`weights/best.onnx`).
- [x] **Tối ưu hóa đa nền tảng:**
  - 🚀 **Local GPU:** Tận dụng NVIDIA GeForce RTX 4050 (6GB VRAM) với CUDA 12.1 (độ trễ ~15 - 25ms).
  - ☁️ **Cloud Deployment:** Đóng gói Docker siêu nhẹ, tối ưu RAM để chạy mượt mà trên Render / Hugging Face Spaces.
- [ ] **Phân tích tư thế tập luyện (Pose Estimation):** Theo dõi 33 điểm mốc cơ thể bằng MediaPipe / YOLO-Pose.
- [ ] **Tự động đếm lần lặp (Rep Counter):** Đếm số rep của bài Squat, Bench Press, Bicep Curl theo góc khớp.

---

## 💻 Yêu cầu hệ thống (System Requirements)

| Thành phần | Yêu cầu khuyến nghị |
| :--- | :--- |
| **Hệ điều hành** | Windows 10 / Windows 11 (64-bit) hoặc Linux |
| **Python** | `Python 3.11.x` (Khuyến nghị chuẩn cho AI, PyTorch & MediaPipe) |
| **GPU** | NVIDIA GeForce RTX 4050 (6GB VRAM) hoặc tương đương (Hỗ trợ cả chế độ CPU) |
| **Driver / CUDA** | NVIDIA Driver 556.12+, CUDA Version 12.1 / 12.5 |
| **RAM** | Tối thiểu 8GB RAM (khi chạy local) / 512MB RAM (khi chạy Docker CPU) |

---

## 📦 Thông tin Dataset (Gym Dataset v2)

Dataset được thu thập và tiền xử lý từ Roboflow Universe bao gồm hơn **45.375 ảnh** với **69 nhãn thiết bị gym**:

- **Tập Train:** ~18.089 ảnh
- **Tập Validation:** ~2.260 ảnh
- **Tập Test:** ~1.100 ảnh
- **Danh sách nhãn tiêu biểu:** *Ab Crunch Machine, Arm Curl Machine, Barbell, Bench, Cable Machine, Chest Machine, Dumbbell, Elliptical, Functional Trainer, Kettlebell, Lat Pull Down Machine, Leg Extension Machine, Leg Press Machine, Pull Up Bar, Resistance Bands, Smith Machine, Squat Rack, Treadmill,...*

---

## ⚙️ Cài đặt & Khởi chạy Local

### 1. Khởi tạo môi trường ảo (Virtual Environment)
```powershell
# Tạo môi trường ảo với Python 3.11
py -3.11 -m venv venv

# Kích hoạt môi trường ảo
.\venv\Scripts\activate
```

### 2. Cài đặt PyTorch GPU (CUDA 12.1)
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 3. Cài đặt các thư viện cần thiết
```powershell
pip install -r requirements.txt
```

### 4. Khởi chạy Web App cục bộ
```powershell
python app.py
```
👉 Mở trình duyệt và truy cập: **`http://localhost:8000`**

---

## 🚀 Huấn luyện mô hình (Training)

Để huấn luyện lại mô hình YOLOv8s từ đầu:
```powershell
python train.py
```

### Cấu hình huấn luyện tối ưu trong `train.py`:
```python
results = model.train(
    data="Gym-Dataset-2/data.yaml",
    epochs=30,          # 30 chu kỳ huấn luyện
    imgsz=640,          # Kích thước ảnh đầu vào tiêu chuẩn
    batch=8,            # Tối ưu cho 6GB VRAM
    device=0,           # ID GPU RTX 4050
    workers=2,          # Nạp dữ liệu ổn định trên Windows
    project="GymAI_App",# Thư mục lưu checkpoint
    name="run_01"
)
```

---

## 📊 Kết quả huấn luyện (Final Benchmarks - 30 Epochs)

*Mô hình **YOLOv8s** sau 30 chu kỳ huấn luyện trên 69 lớp thiết bị Gym:*

| Chỉ số (Metric) | Kết quả đạt được | Đánh giá |
| :--- | :---: | :--- |
| **mAP@0.5** | **82.78%** | Nhận diện rất nhạy và chính xác cao |
| **mAP@0.5:0.95** | **65.26%** | Độ khớp Bounding Box chuẩn xác |
| **Precision** | **80.13%** | Ít dương tính giả (false positive) |
| **Recall** | **76.28%** | Bắt trọn hầu hết các thiết bị trong khung hình |
| **Tốc độ Inference (GPU)** | **~15 - 25 ms** | Đạt chuẩn 40 - 60 FPS thời gian thực |
| **Dung lượng Model** | **22.5 MB** (`best.pt`) | Nhẹ, dễ dàng đóng gói và deploy |

---

## ☁️ Triển khai Cloud (Deployment)

Dự án đã sẵn sàng cho Docker và các nền tảng Cloud:

- **Render / Railway:** Đã cấu hình sẵn `render.yaml`, `Dockerfile` (PyTorch CPU-only siêu nhẹ).
- **Hugging Face Spaces:** Hỗ trợ Docker runtime mặc định (cổng 7860/10000).
- **Live URL:** **[https://gym-ai-project-44yz.onrender.com/](https://gym-ai-project-44yz.onrender.com/)**

---

## 🗺️ Lộ trình phát triển (Roadmap)

- [x] Thu thập & tiền xử lý dataset 69 thiết bị Gym từ Roboflow.
- [x] Huấn luyện hoàn tất 30 epochs YOLOv8s với GPU RTX 4050 (**mAP50 82.8%**).
- [x] Xuất mô hình ONNX (`weights/best.onnx`).
- [x] Xây dựng Web App Responsive kiểm thử Camera & Upload ảnh.
- [x] Deploy ứng dụng lên Render với chứng chỉ HTTPS.
- [ ] Tích hợp MediaPipe Pose để đo góc khớp tay, chân, lưng trong các bài tập phổ biến.
- [ ] Xây dựng logic đếm Reps và cảnh báo sai tư thế bài tập.
