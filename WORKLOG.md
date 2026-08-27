# 📜 NHẬT KÝ PHÁT TRIỂN DỰ ÁN (WORKLOG) - GYM AI

> Tài liệu ghi chép toàn bộ tiến độ, lịch sử các phiên làm việc, lỗi kỹ thuật và giải pháp xử lý, cùng chỉ số huấn luyện của hệ thống Gym AI.

---

## 📑 Mục lục các phiên làm việc (Session Index)
- [📅 2026-08-28: Hoàn tất 30 Epochs Huấn luyện (mAP50 82.8%) & Phát triển Web App Test](#-2026-08-28---hoàn-tất-30-epochs-huấn-luyện-map50-828--phát-triển-web-app-test)
- [📅 2026-08-27: Thiết lập môi trường CUDA, Sửa lỗi Windows MAX_PATH & Huấn luyện YOLOv8s](#-2026-08-27---thiết-lập-môi-trường-cuda-sửa-lỗi-windows-max_path--huấn-luyện-yolov8s-run-01)

---

## 📅 2026-08-28 - Hoàn tất 30 Epochs Huấn luyện (mAP50 82.8%) & Phát triển Web App Test

### 🎯 Mục tiêu phiên làm việc
1. Hoàn tất toàn bộ 30 epochs huấn luyện mô hình YOLOv8s trên 69 lớp thiết bị Gym.
2. Xây dựng ứng dụng Web responsive hỗ trợ Real-time Camera Stream và Upload ảnh để test kiểm thử mô hình trực tiếp.

---

### ✅ Công việc đã hoàn thành
- [x] **Hoàn tất 30 Epochs Huấn luyện:** Mô hình đạt **mAP50 = 82.8%**, **Precision = 80.1%**, **Recall = 76.3%**, lưu trọng số tốt nhất tại `runs/detect/GymAI_App/run_01-2/weights/best.pt`.
- [x] **Xây dựng Backend FastAPI (`app.py`):** Cung cấp các API `/api/detect-frame` (real-time stream) và `/api/detect-image` (upload ảnh), tích hợp GPU RTX 4050 tăng tốc suy luận dưới 25ms.
- [x] **Xây dựng Giao diện Web Responsive (`templates/index.html`, `static/css/style.css`, `static/js/app.js`):**
  - Giao diện Dark Cyberpunk / Gym Aesthetic hiện đại, mượt mà.
  - Tab 📷 **Camera Trực tiếp:** Nhận diện 60 FPS với bounding boxes, nhãn lớp và HUD đo độ trễ/FPS.
  - Tab 🖼️ **Tải ảnh lên:** Kéo thả ảnh (Drag & Drop), thanh trượt điều chỉnh Confidence (10% - 95%), danh sách thẻ thiết bị phát hiện được.
  - Kho ảnh mẫu (Sample Images) từ tập Test để thử nghiệm với 1 cú click.
- [x] **Khởi chạy máy chủ Web thành công:** Sẵn sàng tại `http://localhost:8000`.

---

### 📈 Kết quả huấn luyện cuối cùng (Final Benchmark - Epoch 30)
> **Mô hình:** YOLOv8s | **Tập dữ liệu:** 45.375 ảnh (69 Classes) | **Checkpoints:** `best.pt` (22.5 MB)

| Metric | Kết quả đạt được |
| :--- | :--- |
| **mAP@0.5** | **82.78%** |
| **mAP@0.5:0.95** | **65.26%** |
| **Precision** | **80.13%** |
| **Recall** | **76.28%** |
| **Tốc độ suy luận (Inference)** | **~15 - 25 ms / frame (trên RTX 4050)** |

---

## 📅 2026-08-27 - Thiết lập môi trường CUDA, Sửa lỗi Windows MAX_PATH & Huấn luyện YOLOv8s Run 01

### 🎯 Mục tiêu phiên làm việc
1. Cấu hình môi trường Python hỗ trợ GPU NVIDIA RTX 4050 (6GB VRAM) với CUDA 12.1.
2. Tải và xử lý dataset 69 lớp thiết bị Gym từ Roboflow (`Gym-Dataset-2`).
3. Khởi chạy huấn luyện mô hình phát hiện thiết bị YOLOv8s.
4. Xây dựng bộ skill tự động hóa quản lý dự án (`update-readme`, `update-worklog`).

---

### ✅ Công việc đã hoàn thành
- [x] **Cài đặt Python 3.11.9 & PyTorch CUDA 12.1:** Thay thế Python 3.14.2 cũ (chưa có wheel tương thích với PyTorch), kích hoạt thành công GPU RTX 4050.
- [x] **Xử lý toàn bộ 45.375 file dữ liệu Dataset:** Giải nén hoàn chỉnh 913MB zip từ Roboflow, khắc phục triệt để lỗi nghẽn 19% do Windows giới hạn 260 ký tự.
- [x] **Sửa đường dẫn `data.yaml`:** Đồng bộ các đường dẫn `train`, `val`, `test` trỏ đúng vào thư mục con trong `Gym-Dataset-2`.
- [x] **Cấu hình IDE Language Server:** Tạo `pyrightconfig.json` và `.vscode/settings.json` giúp IDE nhận diện chính xác interpreter trong `venv`.
- [x] **Khởi chạy Huấn luyện YOLOv8s:** Huấn luyện 30 epochs trên RTX 4050 với `batch=8`, `workers=2`, `imgsz=640`.
- [x] **Tạo Workspace Skills:** Tích hợp `update-readme` và `update-worklog` vào `.agents/skills/`.

---

### 🐞 Vấn đề kỹ thuật & Giải pháp (Bug Tracking & Root Cause Analysis)

| # | Vấn đề / Thông báo lỗi | Nguyên nhân gốc rễ | Giải pháp áp dụng | Trạng thái |
| :-: | :--- | :--- | :--- | :---: |
| 1 | `Could not find a version that satisfies the requirement torch` | Máy đang dùng Python 3.14.2, PyTorch hiện chưa build wheel cho bản này. | Cài Python 3.11.9 qua winget, tạo lại `venv` với Python 3.11. | ✅ Đã giải quyết |
| 2 | `Extracting Dataset Version Zip ... 19%` bị văng lỗi `FileNotFoundError / OSError` | Tên một số file ảnh từ Roboflow dài >230 ký tự, cộng đường dẫn thư mục vượt quá giới hạn 260 ký tự (`MAX_PATH`) của Windows. | Dùng script giải nén với prefix mở rộng `\\?\` và đổi tên rút gọn cho 6 file dài bất thường. | ✅ Đã giải quyết |
| 3 | Lỗi sai đường dẫn ảnh khi YOLO nạp `data.yaml` | `data.yaml` mặc định ghi `../train/images` thay vì `train/images`. | Cập nhật lại đường dẫn tương đối chuẩn trong `data.yaml`. | ✅ Đã giải quyết |
| 4 | Cảnh báo IDE `Cannot find module roboflow` | IDE linter dò tìm module theo Python 3.14 toàn cục thay vì `venv`. | Thêm `pyrightconfig.json` & `.vscode/settings.json`, chuyển import roboflow vào bên trong hàm kiểm tra. | ✅ Đã giải quyết |

---

### 📈 Chỉ số huấn luyện mô hình (Training Metrics - YOLOv8s)
> **Phiên:** `GymAI_App/run_01-2` | **Batch:** 8 | **ImgSz:** 640 | **GPU:** RTX 4050 (VRAM chiếm ~2.0 GB / 6 GB)

| Epoch | Thời gian/Epoch | Box Loss | Class Loss | Precision (B) | Recall (B) | mAP50 (B) | mAP50-95 (B) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1/30 | 332s | 1.058 | 3.248 | 0.549 | 0.226 | 0.222 | 0.146 |
| 2/30 | 324s | 0.896 | 2.039 | 0.552 | 0.325 | 0.335 | 0.226 |
| 3/30 | 341s | 0.874 | 1.782 | 0.583 | 0.351 | 0.395 | 0.275 |
| 4/30 | 321s | 0.842 | 1.607 | 0.686 | 0.395 | 0.448 | 0.312 |
| 5/30 | 329s | 0.806 | 1.460 | 0.634 | 0.480 | 0.525 | 0.375 |
| 6/30 | 315s | 0.789 | 1.354 | 0.714 | 0.487 | 0.547 | 0.393 |
| 7/30 | 313s | 0.768 | 1.259 | 0.611 | 0.549 | 0.573 | 0.419 |
| 8/30 | 314s | 0.741 | 1.194 | 0.655 | 0.588 | **0.594** | **0.436** |

---

### ⏭️ Kế hoạch tiếp theo (Next Action Items)
- [ ] Theo dõi hoàn thành đủ 30 epochs (ước tính tổng thời gian ~ 2.5 giờ).
- [ ] Kiểm tra kết quả ma trận nhầm lẫn (`confusion_matrix.png`) và các đồ thị F1-Score trong `runs/detect/GymAI_App/run_01-2/`.
- [ ] Xây dựng file `detect_webcam.py` để test mô hình `best.pt` trực tiếp trên video thực tế.
- [ ] Thiết kế kiến trúc tích hợp mô-đun MediaPipe Pose Estimation vào dự án.
