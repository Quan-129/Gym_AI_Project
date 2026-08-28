---
name: update-context
description: >-
  Use this skill when starting a new conversation, reloading the window, resuming work, or when asked to sync, update, or restore project context from WORKLOG.md, README.md, data.yaml, machine animations, and git history.
---

# Skill: Đồng bộ & Khôi phục Ngữ cảnh Dự án (Update Context)

Skill này giúp Agent nhanh chóng nắm bắt 100% ngữ cảnh lịch sử của dự án **Gym AI** qua các phiên làm việc trước đó, ngay cả khi người dùng khởi động lại cửa sổ chat, mở phiên mới hoặc chuyển đổi môi trường.

---

## 📋 Quy trình thực hiện (Step-by-Step Workflow)

Khi được gọi (hoặc qua lệnh `/update-context`), Agent cần thực hiện tuần tự 4 bước sau:

### Bước 1: Đọc và Tổng hợp Tài liệu Dự án
1. **Đọc [README.md](file:///c:/Users/Acer/Documents/D%E1%BB%B1%20%C3%A1n%20ma/Gym_AI_Project/README.md)**:
   - Nắm bắt mô hình kiến trúc: YOLOv8s nhận diện **69 loại thiết bị & máy gym**.
   - Trọng số và định dạng: `weights/best.pt` (PyTorch) và `weights/best.onnx` (ONNX).
   - Chỉ số Benchmark: **mAP50 = 82.8%**, Precision = 80.1%, Recall = 76.3%.
   - Đường dẫn Cloud Production hiện tại:
     - 🚀 **Railway (Primary - Siêu tốc ~215ms):** `https://gym-ai-vision-production.up.railway.app/`
     - 🌐 **Render (Mirror):** `https://gym-ai-project-44yz.onrender.com/`

2. **Đọc [WORKLOG.md](file:///c:/Users/Acer/Documents/D%E1%BB%B1%20%C3%A1n%20ma/Gym_AI_Project/WORKLOG.md)**:
   - Đọc các phiên làm việc gần nhất để nắm các tính năng vừa phát triển.
   - Đọc bảng **Bug Tracking & Root Cause Analysis** để không lặp lại các lỗi kỹ thuật đã xử lý trong quá khứ (ví dụ: lỗi RAM Render 512Mi, lỗi Unicode Charset Windows, lỗi giật lag camera di động, lỗi linter CSS,...).

---

### Bước 2: Kiểm tra Tài nguyên & Dữ liệu Thực tế trong Codebase
Agent kiểm tra nhanh các thành phần cốt lõi:
1. **Thư viện Video Hoạt Hình (`machine-animation/`)**:
   - Quét các thư mục con: `cardio/`, `arms-core/`, `cable-machines/`, `freeWeights-Acessories/`, `lower-body/`, `upper-body/`.
   - Nắm danh sách các file video `.mp4` đã có để phục vụ tính năng phát video hướng dẫn bài tập.
2. **Cấu hình Backend (`app.py`)**:
   - Kiểm tra các cổng kết nối, API `/api/detect-frame`, `/api/detect-image`, `/api/machine-animations`.
3. **Môi trường & Trọng số AI**:
   - Kiểm tra file `weights/best.pt` và phiên bản `yolov8s.pt`.
   - Kiểm tra `Gym-Dataset-2/data.yaml` (69 classes).

---

### Bước 3: Kiểm tra Trạng thái Git & Đồng bộ Remote
Chạy lệnh kiểm tra nhanh:
```powershell
git status
git log -n 3 --oneline
```
- Đảm bảo branch `main` luôn đồng bộ với remote `origin/main` trên GitHub `Quan-129/Gym_AI_Project`.

---

### Bước 4: Báo cáo Tóm tắt Ngữ cảnh cho Người Dùng
Xuất bản tóm tắt súc tích, ngắn gọn bằng Tiếng Việt gồm:
1. 📌 **Trạng thái hiện tại của dự án** (Mô hình, Web App, Tốc độ suy luận).
2. 🚀 **Trạng thái máy chủ Cloud** (Link Railway đang chạy 24/7).
3. 🎬 **Tài nguyên Media / Hoạt hình** (Số lượng video trong `machine-animation/`).
4. ⏭️ **Kế hoạch tiếp theo (Next Action Items)** sẵn sàng thực hiện theo yêu cầu người dùng.
