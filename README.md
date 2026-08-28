---
title: Gym AI Vision - 69 Equipment Detector
emoji: 🏋️‍♂️
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app_gradio.py
pinned: false
license: mit
---

# 🏋️‍♂️ Gym AI Project - Intelligent Gym Equipment & Workout Assistant

[![Railway Live Demo](https://img.shields.io/badge/Railway-Live%20Demo%20(Fast)-0B0D0E.svg?style=for-the-badge&logo=railway&logoColor=white)](https://gym-ai-vision-production.up.railway.app/)
[![Render Mirror](https://img.shields.io/badge/Render-Mirror%20Server-46E3B7.svg?style=for-the-badge&logo=render&logoColor=white)](https://gym-ai-project-44yz.onrender.com/)
[![Python Version](https://img.shields.io/badge/Python-3.11.9-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.5.1%2Bcu121-EE4C2C.svg?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Ultralytics YOLOv8](https://img.shields.io/badge/YOLOv8-8.4.130-00FFFF.svg?style=for-the-badge)](https://github.com/ultralytics/ultralytics)
[![Hardware](https://img.shields.io/badge/GPU-RTX%204050%206GB-76B900.svg?style=for-the-badge&logo=nvidia&logoColor=white)](https://www.nvidia.com/)
[![License](https://img.shields.io/badge/Dataset-Roboflow%20CC%20BY%204.0-FF6F00.svg?style=for-the-badge)](https://universe.roboflow.com/akash-edwin-samuel/gym-dataset-zfznf/dataset/2)

> **Gym AI** là dự án thị giác máy tính thông minh (Computer Vision AI) hỗ trợ nhận diện **69 loại thiết bị và dụng cụ phòng gym** theo thời gian thực. Dự án tích hợp Web App tương tác trực quan qua Camera & Tải ảnh, đồng thời xây dựng nền tảng cho việc tự động phân tích tư thế tập luyện (Pose Estimation) và đếm số lần tập (Rep Counting).

🚀 **Trải nghiệm trực tiếp trên Web (Railway Cloud 24/7):** **[https://gym-ai-vision-production.up.railway.app/](https://gym-ai-vision-production.up.railway.app/)**  
*(Dự phòng: [Render Server](https://gym-ai-project-44yz.onrender.com/))*

---

## 📌 Tính năng chính (Key Features)

- [x] **Nhận diện 69 lớp thiết bị Gym:** Nhận diện chính xác máy tập, tạ đơn, tạ đòn, máy kéo cáp, máy chạy bộ, xe đạp tập,... (**mAP50 đạt 82.8%**).
- [x] **Web App Responsive Hiện đại:** 
  - 📷 **Live Camera Stream:** Nhận diện thời gian thực qua webcam laptop/điện thoại, đo FPS và độ trễ AI (Latency ms).
  - 🖼️ **Image Drag & Drop:** Kéo thả tải ảnh lên để test, tích hợp kho ảnh mẫu (Sample Images) test nhanh với 1 click.
  - 🎛️ **Điều khiển linh hoạt:** Tùy chỉnh thanh trượt Confidence Threshold (10% - 95%) và IoU NMS.
  - 📊 **Thanh tiến trình & Radar Scanner:** Hiển thị tiến trình nạp ảnh và radar quét thiết bị theo phong cách Cyberpunk.
- [x] **Hỗ trợ đa định dạng mô hình:** Cung cấp cả trọng số **PyTorch** (`weights/best.pt`), **ONNX** (`weights/best.onnx`), và giao diện **Gradio** (`app_gradio.py`).
- [x] **Tối ưu hóa đa nền tảng:**
  - 🚀 **Local GPU:** Tận dụng NVIDIA GeForce RTX 4050 (6GB VRAM) với CUDA 12.1 (độ trễ ~15 - 25ms).
  - ☁️ **Cloud Deployment:** Triển khai độc lập 24/7 trên **Railway Cloud** (suy luận siêu tốc **~215ms**).
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

### 📋 Danh mục 69 loại thiết bị & máy tập Gym được nhận diện:

#### 🏃‍♂️ 1. Nhóm Máy Tập Cardio (Đốt mỡ & Tim mạch)
| Tên thiết bị (Tiếng Anh) | Tên tiếng Việt / Chức năng |
| :--- | :--- |
| **Treadmill** | Máy chạy bộ điện |
| **Stationary Bike** | Xe đạp tập thể lực đứng |
| **Recumbent Bike** | Xe đạp tập có tựa lưng |
| **Elliptical / Cross-trainer** | Máy tập đi bộ trên không (Elip) |
| **Stair Climber** | Máy leo cầu thang |

#### 🏋️ 2. Nhóm Máy Tập Cơ Chân, Mông & Đùi (Lower Body)
| Tên thiết bị (Tiếng Anh) | Tên tiếng Việt / Chức năng |
| :--- | :--- |
| **Leg Press / Leg Press Machine** | Máy đạp đùi (Leg Press nghiêng 45 độ) |
| **Hack Squat Machine** | Máy gánh đùi xiên Hack Squat |
| **Squat Rack** | Khung gánh tạ Squat tự do |
| **Smith Machine** | Máy gánh tạ khung ray trượt an toàn |
| **Leg Extension Machine** | Máy đá đùi trước |
| **Leg Curl Machine / Hamstring Curl** | Máy móc đùi sau (nằm/ngồi) |
| **Hip Adduction Machine** | Máy ép/mở đùi trong và đùi ngoài |
| **Glute Drive Machine** | Máy đẩy hông tập mông (Hip Thrust Machine) |
| **Seated Calf Raise Machine** | Máy nhón bắp chân ngồi |

#### 💪 3. Nhóm Máy Tập Ngực, Vai & Lưng Xô (Upper Body)
| Tên thiết bị (Tiếng Anh) | Tên tiếng Việt / Chức năng |
| :--- | :--- |
| **Chest Machine** | Máy đẩy ngực / ép ngực (Chest Press / Pec Fly) |
| **Shoulder Press Machine** | Máy đẩy vai ngồi |
| **Lateral Raise Machine** | Máy tập cơ vai ngang |
| **Lat Pull Down Machine** | Máy kéo xô lưng thẳng |
| **Seated Row Machine** | Máy chèo thuyền kéo lưng xô ngồi |
| **Back Extension Machine** | Máy gập duỗi lưng dưới (Hyperextension) |

#### 🦾 4. Nhóm Máy Tập Tay & Cơ Bụng (Arms & Core)
| Tên thiết bị (Tiếng Anh) | Tên tiếng Việt / Chức năng |
| :--- | :--- |
| **Arm Curl Machine** | Máy cuốn bắp tay trước |
| **Preacher Curl** | Ghế / máy dốc tập bắp tay trước (Preacher) |
| **Triceps Extension Machine** | Máy duỗi bắp tay sau |
| **Seated Dip Machine** | Máy nhấn xà tập cơ tay sau & ngực dưới |
| **Ab Crunch Machine** | Máy gập bụng có tải trọng tạ |
| **Ab Roller** | Con lăn tập cơ bụng |
| **Leg Raise Tower / Roman Chair / GHD** | Tháp đu xà kép nâng gối / Ghế La Mã tập bụng |

#### ⛓️ 5. Khung Cáp Đa Năng & Các Đầu Kéo Cáp (Cable Machines)
| Tên thiết bị (Tiếng Anh) | Tên tiếng Việt / Chức năng |
| :--- | :--- |
| **Cable Machine / Functional Trainer** | Dàn máy kéo cáp đa năng 2 bên |
| **Multi-Station Home Gym Machine** | Giàn tập tạ khối đa năng tổng hợp |
| **V-Bar Cable Attachment** | Tay nắm kéo cáp chữ V |
| **Straight Bar Attachment** | Thanh đòn thẳng kéo cáp |
| **EZ Bar Cable Attachment** | Thanh đòn uốn lượn ziczac kéo cáp |
| **Single Cable Rope Attachment** | Dây thừng kéo cáp tập tay sau/bụng |
| **Wide Grip / Close Grip Cable Attachment**| Thanh kéo xô rộng / hẹp |
| **Mag Cable Attachment** | Tay cầm kéo xô công thái học (MAG Grip) |

#### 🥊 6. Tạ Tự Do & Dụng Cụ Thể Lực (Free Weights & Accessories)
| Tên thiết bị (Tiếng Anh) | Tên tiếng Việt / Chức năng |
| :--- | :--- |
| **Dumbbell** | Tạ đơn (tạ tay các mức kg) |
| **Barbell** | Tạ đòn dài tiêu chuẩn Olympic |
| **Kettlebell** | Tạ bình vôi (tạ chuông quai cầm) |
| **Plates** | Bánh tạ đĩa (tạ đĩa gang / cao su) |
| **Bench** | Ghế tập tạ (ghế phẳng, ghế dốc lên, dốc xuống) |
| **Pull Up Bar / Parallel Bars** | Xà đơn / Xà kép |
| **Assisted Pull Up and Dip Machine** | Máy trợ lực kéo xà đơn & xà kép |
| **Punching Bag** | Bao cát boxing |
| **Resistance Bands** | Dây thun kháng lực cao su |
| **Plyometric Box** | Hộp gỗ nhảy bật thể lực |
| **Ball** | Bóng tập thể lực (Gym Ball / Slam Ball) |
| **Push Up Equipment** | Dụng cụ hỗ trợ chống đẩy |
| **Foam Equipment** | Con lăn bọt giãn cơ (Foam Roller) |

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
# Khởi chạy FastAPI App
python app.py

# Hoặc khởi chạy giao diện Gradio
python app_gradio.py
```
👉 Mở trình duyệt và truy cập: **`http://localhost:8000`** (FastAPI) hoặc **`http://localhost:7860`** (Gradio).

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
| **Tốc độ Inference (GPU RTX 4050)** | **~15 - 25 ms** | Đạt chuẩn 40 - 60 FPS thời gian thực |
| **Tốc độ Inference (Railway Cloud CPU)** | **~215 ms** | Phản hồi tức thì trên máy chủ Cloud |
| **Dung lượng Model** | **22.5 MB** (`best.pt`) | Nhẹ, dễ dàng đóng gói và deploy |

---

## ☁️ Triển khai Cloud (Deployment)

Dự án đã sẵn sàng cho Docker và các nền tảng Cloud:

- 🚀 **Railway (Primary):** **[https://gym-ai-vision-production.up.railway.app/](https://gym-ai-vision-production.up.railway.app/)** *(Phản hồi siêu tốc 215ms, chạy 24/7 độc lập)*.
- 🌐 **Render (Mirror):** **[https://gym-ai-project-44yz.onrender.com/](https://gym-ai-project-44yz.onrender.com/)**
- **Docker Ready:** Cung cấp sẵn `Dockerfile`, `render.yaml`, `requirements.txt`.

---

## 🗺️ Lộ trình phát triển (Roadmap)

- [x] Thu thập & tiền xử lý dataset 69 thiết bị Gym từ Roboflow.
- [x] Huấn luyện hoàn tất 30 epochs YOLOv8s với GPU RTX 4050 (**mAP50 82.8%**).
- [x] Xuất mô hình ONNX (`weights/best.onnx`).
- [x] Xây dựng Web App Responsive kiểm thử Camera & Upload ảnh.
- [x] Tích hợp thanh tiến trình động & Radar Spinner theo dõi nạp ảnh AI.
- [x] Triển khai Cloud Server 24/7 độc lập trên **Railway** & **Render**.
- [ ] Tích hợp MediaPipe Pose để đo góc khớp tay, chân, lưng trong các bài tập phổ biến.
- [ ] Xây dựng logic đếm Reps và cảnh báo sai tư thế bài tập.
