from ultralytics import YOLO
from pathlib import Path
import cv2
import os
import yaml

def predict_and_save(model, image_path, output_path, output_path_txt):
    results = model.predict(image_path, conf=0.5)
    result = results[0]
    img = result.plot()
    cv2.imwrite(str(output_path), img)
    with open(output_path_txt, 'w') as f:
        for box in result.boxes:
            cls_id = int(box.cls)
            x_center, y_center, width, height = box.xywhn[0].tolist()
            f.write(f"{cls_id} {x_center} {y_center} {width} {height}\n")

if __name__ == '__main__':
    this_dir = Path(__file__).parent
    os.chdir(this_dir)
    
    with open(this_dir / 'yolo_params.yaml', 'r') as file:
        data = yaml.safe_load(file)
        if 'test' in data and data['test'] is not None:
            images_dir = Path(data['test']) / 'images'
        else:
            print("No test field found")
            exit()
    
    if not images_dir.exists():
        print(f"Images directory {images_dir} does not exist")
        exit()
    
    best_model_path = None
    possible_paths = [
        Path("C:/Users/ASUS/runs/detect/train/weights/best.pt"),
        this_dir / "runs" / "detect" / "train" / "weights" / "best.pt",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            best_model_path = path
            print(f"Found model: {best_model_path}")
            break
    
    if best_model_path is None:
        print("Could not find best.pt!")
        exit()
    
    model = YOLO(best_model_path)
    
    predictions_dir = this_dir / 'predictions'
    predictions_dir.mkdir(exist_ok=True)
    (predictions_dir / 'images').mkdir(exist_ok=True)
    (predictions_dir / 'labels').mkdir(exist_ok=True)
    
    image_files = list(images_dir.glob('*.png')) + list(images_dir.glob('*.jpg'))
    total = len(image_files)
    
    print(f"Processing {total} images...")
    for idx, img_path in enumerate(image_files, 1):
        out_img = predictions_dir / 'images' / img_path.name
        out_txt = predictions_dir / 'labels' / (img_path.stem + '.txt')
        predict_and_save(model, img_path, out_img, out_txt)
        if idx % 10 == 0:
            print(f"  {idx}/{total} done")
    
    print(f"Complete! Predictions in: {predictions_dir}")
