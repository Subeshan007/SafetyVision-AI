# EMERGENCY: Optimized training configuration for 13-hour deadline
# This will maximize accuracy while minimizing training time

EPOCHS = 50              # Good balance for overnight
BATCH = 16               # Optimal for RTX 3060 6GB
IMGSZ = 640              # Standard size
DEVICE = 0               # Force GPU

# OPTIMIZED HYPERPARAMETERS FOR HIGH ACCURACY
LR0 = 0.01               # Higher initial LR for faster convergence
LRF = 0.0001             # Strong decay
MOMENTUM = 0.937         # Standard for YOLO
WEIGHT_DECAY = 0.0005

# AGGRESSIVE AUGMENTATION FOR BETTER GENERALIZATION
OPTIMIZER = 'SGD'        # Often best for YOLO
MOSAIC = 0.8             # Strong augmentation
MIXUP = 0.15             # Helps with difficult cases
FLIPUD = 0.0
FLIPLR = 0.5
HSV_H = 0.015
HSV_S = 0.7
HSV_V = 0.4

# WARMUP SETTINGS
WARMUP_EPOCHS = 3.0
WARMUP_MOMENTUM = 0.8
WARMUP_BIAS_LR = 0.1

# ADVANCED SETTINGS
CLOSE_MOSAIC = 10        # Disable mosaic in last 10 epochs
PATIENCE = 50            # Don't stop early

import argparse
from ultralytics import YOLO
import os
import sys
import torch

if __name__ == '__main__': 
    # Verify GPU
    if torch.cuda.is_available():
        print(f"✅ GPU DETECTED: {torch.cuda.get_device_name(0)}")
        print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("⚠️ WARNING: GPU NOT DETECTED! Training will be VERY SLOW!")
        print("   Run EMERGENCY_GPU_SETUP.bat first!")
        input("Press Enter to continue with CPU (not recommended) or Ctrl+C to abort...")
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=EPOCHS, help='Number of epochs')
    parser.add_argument('--batch', type=int, default=BATCH, help='Batch size')
    parser.add_argument('--imgsz', type=int, default=IMGSZ, help='Image size')
    parser.add_argument('--device', default=DEVICE, help='Device (0 for GPU, cpu for CPU)')
    args = parser.parse_args()
    
    this_dir = os.path.dirname(__file__)
    if not this_dir:
        this_dir = os.getcwd()
    os.chdir(this_dir)
    
    # Check for weights
    weights_path = os.path.join(this_dir, "yolov8s.pt")
    if not os.path.exists(weights_path):
        print("\n⚠️ ERROR: yolov8s.pt not found!")
        print("   Downloading automatically...")
        model = YOLO("yolov8s.pt")  # Will download automatically
    else:
        model = YOLO(weights_path)
    
    print("\n" + "="*60)
    print("🚀 EMERGENCY TRAINING - OPTIMIZED FOR HIGH ACCURACY")
    print("="*60)
    print(f"Epochs: {args.epochs}")
    print(f"Batch Size: {args.batch}")
    print(f"Image Size: {args.imgsz}")
    print(f"Learning Rate: {LR0} → {LRF}")
    print(f"Augmentation: Mosaic={MOSAIC}, Mixup={MIXUP}")
    print(f"Device: {args.device}")
    print("="*60 + "\n")
    
    # OPTIMIZED TRAINING
    results = model.train(
        data=os.path.join(this_dir, "yolo_params.yaml"), 
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        
        # Optimizer settings
        optimizer=OPTIMIZER,
        lr0=LR0,
        lrf=LRF,
        momentum=MOMENTUM,
        weight_decay=WEIGHT_DECAY,
        
        # Augmentation
        mosaic=MOSAIC,
        mixup=MIXUP,
        flipud=FLIPUD,
        fliplr=FLIPLR,
        hsv_h=HSV_H,
        hsv_s=HSV_S,
        hsv_v=HSV_V,
        
        # Warmup
        warmup_epochs=WARMUP_EPOCHS,
        warmup_momentum=WARMUP_MOMENTUM,
        warmup_bias_lr=WARMUP_BIAS_LR,
        
        # Advanced
        close_mosaic=CLOSE_MOSAIC,
        patience=PATIENCE,
        
        # Performance
        save=True,
        save_period=-1,  # Only save last and best
        plots=True,
        verbose=True
    )
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE!")
    print("="*60)
    print(f"Best model saved to: runs/detect/train/weights/best.pt")
    print("\nNext step: Run predict.py to evaluate")
    print("="*60)
