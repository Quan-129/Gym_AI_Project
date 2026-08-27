# 🏋️‍♂️ Gym AI Project - Intelligent Gym Equipment & Workout Assistant

[![Python Version](https://img.shields.io/badge/Python-3.11.9-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.5.1%2Bcu121-red.svg)](https://pytorch.org/)
[![Ultralytics YOLOv8](https://img.shields.io/badge/YOLOv8-8.4.130-brightgreen.svg)](https://github.com/ultralytics/ultralytics)
[![Hardware](https://img.shields.io/badge/GPU-RTX%204050%206GB-76B900.svg)](https://www.nvidia.com/)
[![License](https://img.shields.io/badge/Dataset-Roboflow%20CC%20BY%204.0-orange.svg)](https://universe.roboflow.com/akash-edwin-samuel/gym-dataset-zfznf/dataset/2)

> **Gym AI** là dự án thị giác máy tính thông minh (Computer Vision AI) hỗ trợ nhận diện **69 loại thiết bị và dụng cụ phòng gym**, xây dựng nền tảng cho việc tự động phân tích tư thế tập luyện (Pose Estimation), đếm số lần tập (Rep Counting) và đánh giá kỹ thuật động tác.

---

## 📌 Tính năng chính (Key Features)

- [x] **Nhận diện 69 lớp thiết bị Gym:** Nhận diện nhanh và chính xác các loại máy tập, tạ đơn, tạ đòn, máy kéo cáp, máy chạy bộ,...
- [x] **Tối ưu hóa phần cứng NVIDIA GPU:** Tận dụng tối đa sức mạnh của NVIDIA GeForce RTX 4050 (6GB VRAM) với CUDA 12.1 và FP16 / AMP.
- [x] **Tự động hóa xử lý dữ liệu:** Quản lý dữ liệu thông minh, tự động giải nén và xử lý an toàn trên Windows.
- [ ] **Phân tích tư thế tập luyện (Pose Estimation):** Theo dõi 33 điểm mốc cơ thể để kiểm tra form tập đúng/sai.
- [ ] **Tự động đếm lần lặp (Rep Counter):** Đếm số rep của bài Squat, Bench Press, Bicep Curl theo quỹ đạo khớp.
- [ ] **Giao diện thời gian thực:** Kết nối trực tiếp Webcam / Camera giám sát phòng gym.

---

## 💻 Yêu cầu hệ thống (System Requirements)

| Thành phần | Yêu cầu khuyến nghị |
| :--- | :--- |
| **Hệ điều hành** | Windows 10 / Windows 11 (64-bit) |
| **Python** | `Python 3.11.9` (Khuyến nghị chuẩn cho AI, PyTorch & MediaPipe) |
| **GPU** | NVIDIA GeForce RTX 4050 Laptop GPU (6GB VRAM) hoặc tương đương |
| **Driver / CUDA** | NVIDIA Driver 556.12+, CUDA Version 12.1 / 12.5 |
| **RAM** | Tối thiểu 16GB RAM |
| **Dung lượng ổ đĩa** | Trống tối thiểu 10GB cho Dataset & Checkpoints |

---

## 📦 Thông tin Dataset (Gym Dataset v2)

Dataset được xuất bản trên Roboflow Universe bao gồm hơn **45.300+ ảnh** với **69 nhãn thiết bị gym**:

- **Tập Train:** ~18.089 ảnh
- **Tập Validation:** ~2.260 ảnh
- **Tập Test:** ~1.100 ảnh
- **Danh sách nhãn tiêu biểu:** *Dumbbell, Barbell, Treadmill, Bench, Cable Machine, Lat Pull Down, Leg Press, Smith Machine, Squat Rack, Kettlebell, Stationary Bike, Elliptical,...*

---

## ⚙️ Cài đặt môi trường (Setup Guide)

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

### 3. Cài đặt Ultralytics & các thư viện bổ trợ
```powershell
pip install ultralytics roboflow "numpy<2.4,>=1.24" "opencv-python==4.10.0.84"
```

### 4. Kiểm tra GPU nhận diện
```powershell
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0))"
```

---

## 🚀 Huấn luyện mô hình (Training)

Chạy file kịch bản huấn luyện:
```powershell
python train.py
```

### Cấu hình huấn luyện trong `train.py`:
```python
results = model.train(
    data="Gym-Dataset-2/data.yaml",
    epochs=30,          # 30 chu kỳ huấn luyện
    imgsz=640,          # Kích thước ảnh đầu vào tiêu chuẩn
    batch=8,            # Tối ưu cho 6GB VRAM (không bị tràn bộ nhớ)
    device=0,           # ID GPU RTX 4050
    workers=2,          # Đa luồng nạp dữ liệu ổn định trên Windows
    project="GymAI_App",# Thư mục lưu kết quả
    name="run_01"       # Tên phiên huấn luyện
)
```

---

## 🔮 Dự đoán & Kiểm thử (Inference)

Sau khi hoàn tất quá trình huấn luyện, trọng số tốt nhất được lưu tại `runs/detect/GymAI_App/run_01/weights/best.pt`.

### Code Python dự đoán trên ảnh hoặc Webcam:
```python
from ultralytics import YOLO
import cv2

# Nạp mô hình đã train
model = YOLO('runs/detect/GymAI_App/run_01-2/weights/best.pt')

# Dự đoán từ Webcam (source=0) hoặc video
results = model.predict(source=0, show=True, conf=0.5)
```

---

## 📊 Kết quả huấn luyện gần nhất (Benchmarks)

*Tiến trình huấn luyện mô hình **YOLOv8s** trên tập dữ liệu 69 lớp:*

| Epoch | GPU Memory | Box Loss | Class Loss | Precision (B) | Recall (B) | mAP50 (B) | mAP50-95 (B) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ~2.0 GB | 1.058 | 3.248 | 0.549 | 0.226 | 0.222 | 0.146 |
| 3 | ~2.0 GB | 0.874 | 1.782 | 0.583 | 0.351 | 0.395 | 0.275 |
| 5 | ~2.0 GB | 0.806 | 1.460 | 0.634 | 0.480 | 0.525 | 0.375 |
| 7 | ~2.0 GB | 0.768 | 1.259 | 0.611 | 0.549 | 0.573 | 0.419 |
| 8 | ~2.0 GB | 0.741 | 1.194 | 0.655 | 0.588 | **0.594** | **0.436** |

---

## 🗺️ Lộ trình phát triển (Roadmap)

- [x] Thu thập & tiền xử lý dataset 69 thiết bị Gym từ Roboflow.
- [x] Huấn luyện baseline model YOLOv8s với GPU RTX 4050.
- [ ] Hoàn tất 30 epochs & xuất file mô hình ONNX / TensorRT để tăng tốc độ suy luận.
- [ ] Tích hợp MediaPipe Pose để đo góc khớp tay, chân, lưng trong các bài tập phổ biến.
- [ ] Xây dựng logic đếm Reps và cảnh báo sai tư thế.
- [ ] Xây dựng Web App demo tương tác trực quan.
