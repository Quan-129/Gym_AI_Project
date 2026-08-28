---
name: update-readme
description: >-
  Use this skill when the user asks to create, update, format, or synchronize the project's README.md file with the current codebase state, project structure, dataset details, hardware configuration, and training/inference instructions.
---

# Skill: Cập nhật và Đồng bộ README.md cho Gym AI Project

Skill này hướng dẫn quy trình tiêu chuẩn để tạo mới hoặc cập nhật file `README.md` của dự án **Gym AI** một cách chuyên nghiệp, trực quan và luôn đồng bộ với mã nguồn thực tế.

---

## 📋 Quy trình thực hiện (Step-by-Step Workflow)

### Bước 1: Thu thập thông tin thực tế từ dự án
Trước khi viết hoặc cập nhật `README.md`, luôn đọc và kiểm tra các nguồn thông tin sau trong workspace:
1. **Cấu hình Dataset**: Đọc file `Gym-Dataset-2/data.yaml` để lấy danh sách số lượng lớp (`nc`), tên 69 loại thiết bị gym (`names`), đường dẫn `train/val/test`.
2. **Kịch bản huấn luyện**: Đọc `train.py` để lấy các siêu tham số (model `yolov8s.pt`, `epochs`, `batch`, `imgsz`, `device`, `workers`).
3. **Kết quả huấn luyện mới nhất**: Kiểm tra thư mục `runs/detect/GymAI_App/` để đọc file `results.csv` (nếu có), lấy các chỉ số `mAP50`, `Precision`, `Recall`, `Loss`.
4. **Môi trường & Phần cứng**: Kiểm tra phiên bản Python (`Python 3.11`), PyTorch CUDA (`cu121`), thông số GPU (`NVIDIA GeForce RTX 4050 Laptop GPU 6GB VRAM`).

---

### Bước 2: Cấu trúc chuẩn của file `README.md`
File `README.md` cần tuân thủ cấu trúc chuẩn, gồm các phần sau:

```markdown
# 🏋️‍♂️ Gym AI Project - Intelligent Gym Equipment & Workout Assistant

> Hệ thống AI nhận diện 69 loại thiết bị tập gym, hỗ trợ đếm số lần tập (Rep Counting) và phân tích tư thế tập luyện (Pose Estimation) theo thời gian thực.

---

## 📌 Tính năng chính (Key Features)
- [x] Nhận diện 69 loại máy móc & dụng cụ tập gym (Dumbbell, Barbell, Treadmill, Cable Machine,...) bằng YOLOv8s.
- [x] Tối ưu hóa huấn luyện trên GPU NVIDIA RTX 4050 (6GB VRAM).
- [ ] Phân tích khung xương và góc khớp khớp xương bằng MediaPipe / YOLO-Pose.
- [ ] Đếm số lần lặp lại bài tập (Rep Counter) tự động.
- [ ] Giao diện Web App / Mobile App tương tác trực tiếp.

---

## 💻 Yêu cầu hệ thống (System Requirements)
- **Hệ điều hành:** Windows 10/11 64-bit
- **Python:** 3.11.x (Khuyến nghị chuẩn cho AI/MediaPipe/Torch)
- **GPU:** NVIDIA GeForce RTX 4050 (hoặc GPU tương đương có VRAM >= 6GB)
- **CUDA:** 12.1+ / cu121

---

## 📦 Dữ liệu huấn luyện (Dataset Information)
- **Nguồn:** Roboflow Universe (`gym-dataset-zfznf` v2)
- **Số lớp (Classes):** 69 thiết bị & dụng cụ gym
- **Tổng số ảnh:** ~45.375 ảnh (Train: ~18.100 ảnh, Valid: ~2.260 ảnh, Test: ~1.100 ảnh)

---

## ⚙️ Cài đặt môi trường (Setup Guide)
(Hướng dẫn chi tiết từ tạo venv, cài PyTorch GPU đến cài đặt các thư viện cần thiết)

---

## 🚀 Huấn luyện mô hình (Training)
(Lệnh chạy và giải thích các tham số trong train.py)

---

## 🔮 Dự đoán & Kiểm thử (Inference)
(Đoạn code mẫu Python chạy phát hiện trên webcam / video bằng trọng số best.pt)

---

## 📊 Kết quả huấn luyện (Benchmarks & Metrics)
(Bảng tóm tắt chỉ số mAP, Loss qua các Epochs cập nhật từ runs/)

---

## 🗺️ Lộ trình phát triển (Roadmap)
```

---

### Bước 3: Cập nhật và Kiểm tra
1. Sử dụng `write_to_file` (nếu tạo mới) hoặc `replace_file_content` (nếu sửa đổi từng phần).
2. Đảm bảo ngôn ngữ diễn đạt rõ ràng, chuyên nghiệp, sử dụng biểu tượng cảm xúc (emojis) hợp lý để tăng tính trực quan.
3. Luôn kiểm tra các đường dẫn tương đối và đường dẫn file trong tài liệu để không bị lỗi 404.
