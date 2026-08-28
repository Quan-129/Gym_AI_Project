# 📜 NHẬT KÝ PHÁT TRIỂN DỰ ÁN (WORKLOG) - GYM AI

> Tài liệu ghi chép toàn bộ tiến độ, lịch sử các phiên làm việc, lỗi kỹ thuật và giải pháp xử lý, cùng chỉ số huấn luyện của hệ thống Gym AI.

---

## 📑 Mục lục các phiên làm việc (Session Index)
- [📅 2026-08-28 (Chiều/Tối): Tích hợp Video Hoạt Hình Máy Tập, Tối ưu 60 FPS Mobile Camera, Tra Cứu 69 Thiết Bị & Skill Update Context](#-2026-08-28-chiềutối---tích-hợp-video-hoạt-hình-máy-tập-tối-ưu-60-fps-mobile-camera-tra-cứu-69-thiết-bị--skill-update-context)
- [📅 2026-08-28 (Sáng): Hoàn tất 30 Epochs Huấn luyện (mAP50 82.8%) & Triển khai Cloud Railway / Render](#-2026-08-28-sáng---hoàn-tất-30-epochs-huấn-luyện-map50-828--triển-khai-cloud-railway--render)
- [📅 2026-08-27: Thiết lập môi trường CUDA, Sửa lỗi Windows MAX_PATH & Huấn luyện YOLOv8s](#-2026-08-27---thiết-lập-môi-trường-cuda-sửa-lỗi-windows-max_path--huấn-luyện-yolov8s-run-01)

---

## 📅 2026-08-28 (Chiều/Tối) - Tích hợp Video Hoạt Hình Máy Tập, Tối ưu 60 FPS Mobile Camera, Tra Cứu 69 Thiết Bị & Skill Update Context

### 🎯 Mục tiêu phiên làm việc
1. Khắc phục lỗi giật lag và màn hình đen trên trình duyệt điện thoại (iOS / Android) khi phát trực tiếp Camera.
2. Xây dựng Bảng Tra Cứu / Tìm Kiếm trực quan cho toàn bộ 69 danh mục thiết bị Gym.
3. Tích hợp thư viện video hoạt hình hướng dẫn tập luyện (`machine-animation/`) vào cả AI Detection và Bảng tra cứu.
4. Tinh chỉnh giao diện thẻ thiết bị (loại bỏ nút tràn viền, dùng Nút Play Neon nhỏ gọn chuẩn phong cách Fitness hiện đại).
5. Sửa sạch 100% lỗi linter CSS và cảnh báo kiểu dữ liệu Pyright trong `app.py`.
6. Xây dựng Custom Skill `update-context` để Agent luôn đồng bộ trí nhớ dự án qua các phiên làm việc.

---

### ✅ Công việc đã hoàn thành
- [x] **Động cơ Camera 60 FPS Độc lập cho Mobile & Desktop:**
  - Tách luồng vẽ video cục bộ 60 FPS (`renderLocalVideoLoop` với `playsinline webkit-playsinline muted`) khỏi luồng gửi nhận AI.
  - Xây dựng luồng AI Async gửi khung hình nén siêu nhẹ 320x240 (~8KB), trả về tọa độ tỉ lệ `rel_box` để Client tự vẽ Bounding Box Cyberpunk trực tiếp trên Canvas, giảm 90% tải mạng và triệt tiêu giật lag trên điện thoại.
- [x] **Tích hợp Thư viện Video Hoạt hình Hướng dẫn Máy tập (`machine-animation/`):**
  - Mount thư mục tĩnh `/machine-animation` và xây dựng API `/api/machine-animations` tự động quét các thư mục con (`cardio/`, `arms-core/`, `cable-machines/`, `freeWeights-Acessories/`, `lower-body/`, `upper-body/`).
  - Xây dựng Modal Trình phát Video hướng dẫn (`#videoModal`) hỗ trợ phát lặp vô tận (Auto-loop), hiển thị tên tiếng Việt, nhóm cơ và mô tả bài tập.
  - Tự động liên kết: Khi AI nhận diện được máy tập hoặc khi người dùng click vào thẻ trong bảng tra cứu ➔ Bật ngay video hướng dẫn tập của máy đó.
- [x] **Bảng Tra Cứu & Tìm Kiếm 69 Thiết Bị Gym Thông Minh:**
  - Nút bấm phát sáng Neon `[ 69 Thiết Bị Gym • Tra cứu ]` trên thanh điều hướng và chân trang.
  - Hỗ trợ tìm kiếm thời gian thực theo từ khóa Tiếng Việt / Tiếng Anh / Tác dụng cơ bắp, kèm 7 bộ lọc danh mục.
- [x] **Tinh chỉnh Bố cục Thẻ Thiết Bị (Fix UI Squishing & Overflow):**
  - Thay thế nút chữ dài cồng kềnh bằng **Nút Play tròn phát sáng Neon Cyan/Green ở góc trên bên phải thẻ** và huy hiệu Play ở góc Icon.
  - Bố cục 3 dòng (Tên tiếng Anh, Tên tiếng Việt, Mô tả) hiển thị thoáng đãng, sắc nét, không bị che khuất hay chèn ép.
- [x] **Làm sạch Mã nguồn & Sửa Lỗi Linter:**
  - Xóa dấu `}` thừa dòng 785 và thêm thuộc tính W3C `background-clip`, `appearance` trong `style.css` (0 Errors / 0 Warnings).
  - Chuẩn hóa kiểu dữ liệu Pyright trong `app.py` cho `base64.b64encode`, kiểm tra biến `MODEL_PATH` và trích xuất nhãn an toàn từ YOLO `Results`.
- [x] **Phát triển Custom Skill `update-context` (`.agents/skills/update-context/SKILL.md`):**
  - Giúp Agent tự động khôi phục và đồng bộ 100% ngữ cảnh lịch sử dự án khi người dùng reload IDE hoặc gõ `/update-context`.
  - Cập nhật `.gitignore` để lưu vết và đồng bộ các custom skill lên GitHub.

---

### 🐞 Vấn đề kỹ thuật & Giải pháp (Bug Tracking & Root Cause Analysis)

| # | Vấn đề / Thông báo lỗi | Nguyên nhân gốc rễ | Giải pháp áp dụng | Trạng thái |
| :-: | :--- | :--- | :--- | :---: |
| 1 | Camera Live bị lag / đen màn hình trên điện thoại | Trình duyệt Mobile chặn video không có `playsinline` và bị nghẽn do chờ phản hồi base64 qua lại từng khung hình. | Thêm `playsinline webkit-playsinline muted` trên thẻ video; tách luồng render video 60 FPS độc lập với luồng suy luận AI gửi khung hình nén 320x240. | ✅ Đã giải quyết |
| 2 | Nút video bị đè và tràn viền thẻ thiết bị | Nút chữ dài `[ Xem video hoạt hình ]` nằm dưới đáy làm đội chiều cao vượt quá giới hạn grid. | Thay bằng nút Play tròn Neon Cyan/Green nhỏ gọn ở góc trên bên phải thẻ cạnh badge danh mục. | ✅ Đã giải quyết |
| 3 | Lỗi đỏ CSS `at-rule or selector expected` dòng 785 | Thừa một dấu đóng ngoặc `}` sau class `.progress-percent`. | Xóa dấu `}` thừa, bổ sung `background-clip` và `appearance` chuẩn. | ✅ Đã giải quyết |
| 4 | Cảnh báo Pyright Buffer & Results trong `app.py` | OpenCV buffer cần ép kiểu `.tobytes()`, đối tượng YOLO Results cần duyệt danh sách an toàn. | Thêm `.tobytes()` và chuẩn hóa hàm trích xuất thuộc tính `getattr(res0, 'boxes')`. | ✅ Đã giải quyết |

---

## 📅 2026-08-28 (Sáng) - Hoàn tất 30 Epochs Huấn luyện (mAP50 82.8%) & Triển khai Cloud Railway / Render

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
- [x] **Đóng gói & Triển khai Cloud Thành công (Railway & Render Cloud):**
  - Tạo `Dockerfile`, `render.yaml`, `requirements.txt`, đẩy repo lên GitHub `Quan-129/Gym_AI_Project`.
  - Khắc phục lỗi `Out of memory (>512Mi)` bằng cách dùng PyTorch CPU-only và tối ưu kích thước suy luận.
  - Xuất thành công định dạng **ONNX** (`weights/best.onnx` - 42.8 MB) và giao diện **Gradio** (`app_gradio.py`).
  - **🚀 Primary Production URL (Railway - Siêu tốc ~215ms):** **[https://gym-ai-vision-production.up.railway.app/](https://gym-ai-vision-production.up.railway.app/)**
  - **🌐 Backup Mirror (Render):** **[https://gym-ai-project-44yz.onrender.com/](https://gym-ai-project-44yz.onrender.com/)**

---

### 🐞 Vấn đề kỹ thuật & Giải pháp (Bug Tracking & Root Cause Analysis)

| # | Vấn đề / Thông báo lỗi | Nguyên nhân gốc rễ | Giải pháp áp dụng | Trạng thái |
| :-: | :--- | :--- | :--- | :---: |
| 1 | `[Errno 10048] address already in use: 8000` | Cổng 8000 bị chiếm do tiến trình máy chủ trước đó chưa tắt hoàn toàn. | Giải phóng cổng 8000, sửa cú pháp `TemplateResponse` cho Starlette mới. | ✅ Đã giải quyết |
| 2 | `Out of memory (used over 512Mi)` trên Render Free | `pip install torch` mặc định tải bản CUDA nặng 4GB vượt 512MB RAM. | Đổi Dockerfile sang PyTorch CPU-only (~150MB) + giới hạn luồng `torch.set_num_threads(1)`. | ✅ Đã giải quyết |

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
