from ultralytics import YOLO
import os

def main():
    dataset_dir = os.path.abspath("Gym-Dataset-2")
    yaml_path = os.path.join(dataset_dir, "data.yaml")

    if not os.path.exists(yaml_path):
        print("🚀 BẮT ĐẦU TẢI DỮ LIỆU TỪ ROBOFLOW...")
        from roboflow import Roboflow
        rf = Roboflow(api_key="0SsQHoZ0toAufj0IxPyV")
        project = rf.workspace("akash-edwin-samuel").project("gym-dataset-zfznf")
        version = project.version(2)
        dataset = version.download("yolov8")
        yaml_path = os.path.join(dataset.location, "data.yaml")
        print(f"✅ Đã tải xong dữ liệu về: {dataset.location}")
    else:
        print(f"✅ Đã tìm thấy dữ liệu có sẵn tại: {dataset_dir}")

    print("🧠 KHỞI TẠO MÔ HÌNH YOLOv8s...")
    model = YOLO('yolov8s.pt')

    print("🔥 BẮT ĐẦU HUẤN LUYỆN TRÊN RTX 4050...")
    
    # Cấu hình đã được tối ưu cho 6GB VRAM để không bị tràn bộ nhớ
    results = model.train(
        data=yaml_path,
        epochs=30,          # Chạy thử 30 vòng
        imgsz=640,          # Kích thước ảnh chuẩn
        batch=8,            # (QUAN TRỌNG) Giữ ở mức 8 để VRAM không bị quá tải
        device=0,           # ID của card RTX 4050
        workers=2,          # Dùng 2 luồng CPU tối ưu cho Windows
        project="GymAI_App",# Tên thư mục lưu model sau khi train
        name="run_01"       # Tên lần chạy này
    )
    print("🎉 HOÀN TẤT HUẤN LUYỆN!")

if __name__ == '__main__':
    main()