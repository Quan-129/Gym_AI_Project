---
name: update-worklog
description: >-
  Use this skill when the user asks to log progress, record work sessions, document bug fixes, update project milestones, track model training metrics, or maintain the project worklog (WORKLOG.md).
---

# Skill: Ghi chép và Cập nhật Nhật ký Phát triển (WORKLOG.md)

Skill này hướng dẫn quy trình tiêu chuẩn để ghi lại tiến độ dự án **Gym AI**, lưu vết các lỗi kỹ thuật đã xử lý (bug & fixes), theo dõi các chỉ số huấn luyện mô hình YOLOv8, và lập kế hoạch công việc tiếp theo trong file `WORKLOG.md`.

---

## 📋 Quy trình thực hiện (Step-by-Step Workflow)

### Bước 1: Thu thập thông tin phiên làm việc
Trước khi ghi nhật ký, tổng hợp nhanh các thông tin:
1. **Thời gian hiện tại**: Ngày/tháng/năm và giờ ghi nhận.
2. **Các thay đổi trong phiên**:
   - File mã nguồn mới tạo hoặc sửa đổi (`train.py`, `data.yaml`, cấu hình IDE,...).
   - Thư viện / môi trường được cập nhật (`pip install`, phiên bản Python, CUDA,...).
3. **Lỗi kỹ thuật đã gặp và cách khắc phục**:
   - Ghi rõ: Triệu chứng lỗi (Error message) -> Nguyên nhân gốc rễ (Root Cause) -> Giải pháp cụ thể (Fix).
4. **Trạng thái huấn luyện mô hình (nếu có)**:
   - Kiểm tra `runs/detect/GymAI_App/` để lấy epoch mới nhất, `train/box_loss`, `train/cls_loss`, `metrics/mAP50(B)`, `metrics/precision(B)`, `metrics/recall(B)`.
5. **Kế hoạch tiếp theo (Next Action Items)**: Các đầu việc cần làm ở phiên sau.

---

### Bước 2: Định dạng cấu trúc một mục nhật ký (Entry Format)

Luôn thêm mục mới lên **đầu danh sách các phiên** (Reverse Chronological Order - phiên mới nhất ở trên cùng) theo cấu trúc chuẩn sau:

```markdown
## 📅 [YYYY-MM-DD] - Tên tóm tắt phiên làm việc (Ví dụ: Thiết lập môi trường CUDA & Huấn luyện YOLOv8s Run 01)

### 🎯 Mục tiêu phiên làm việc
- Mục tiêu 1...
- Mục tiêu 2...

---

### ✅ Công việc đã hoàn thành
- [x] **Nhiệm vụ 1**: Chi tiết công việc đã thực hiện.
- [x] **Nhiệm vụ 2**: Chi tiết...

---

### 🐞 Vấn đề kỹ thuật & Giải pháp (Bug Tracking & Fixes)
| Vấn đề / Lỗi gặp phải | Nguyên nhân gốc rễ | Giải pháp đã áp dụng | Trạng thái |
| :--- | :--- | :--- | :--- |
| `pip install torch` báo không tìm thấy version | Đang dùng Python 3.14 (chưa có wheel PyTorch) | Chuyển sang Python 3.11.9, tạo lại venv | ✅ Đã xử lý |
| Lỗi giải nén Roboflow zip ở 19% | Windows MAX_PATH (260 chars) bị vượt do tên file dài | Dùng cú pháp `\\?\` giải nén và rút gọn tên file | ✅ Đã xử lý |

---

### 📈 Chỉ số huấn luyện mô hình (Training Metrics)
> **Mô hình:** YOLOv8s | **Tập dữ liệu:** Gym-Dataset-2 (69 classes) | **Phần cứng:** RTX 4050 6GB

| Epoch | GPU Mem | Box Loss | Class Loss | Precision | Recall | mAP50 | mAP50-95 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ~2.0 GB | 1.058 | 3.248 | 0.549 | 0.226 | 0.222 | 0.146 |
| 5 | ~2.0 GB | 0.806 | 1.460 | 0.634 | 0.480 | 0.525 | 0.375 |
| 7 | ~2.0 GB | 0.768 | 1.259 | 0.611 | 0.549 | 0.573 | 0.419 |

---

### ⏭️ Kế hoạch tiếp theo (Next Action Items)
- [ ] Chờ hoàn tất 30 epochs huấn luyện và đánh giá trọng số `best.pt`.
- [ ] Viết kịch bản kiểm thử nhận diện thiết bị trên webcam/video (`predict.py`).
- [ ] Tích hợp mô-đun phân tích tư thế tập gym (Pose Estimation & Rep Counter).
```

---

### Bước 3: Cập nhật và Duy trì file `WORKLOG.md`
1. Nếu file `WORKLOG.md` chưa tồn tại, khởi tạo phần mở đầu (Header, Mô tả dự án, Mục lục tổng quan) rồi chèn entry đầu tiên.
2. Nếu file đã tồn tại, chèn entry mới ngay dưới tiêu đề `# 📜 NHẬT KÝ PHÁT TRIỂN (WORKLOG)`.
3. Kiểm tra tính chính xác của các số liệu và bảng biểu trước khi lưu.
