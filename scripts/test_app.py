"""
Quick Demo - SafetyVision AI App
Tests that the app can be launched and model can be loaded
"""

import sys
from pathlib import Path

print("="*60)
print("SafetyVision AI - Quick Demo Test")
print("="*60)
print()

# Check dependencies
print("Checking dependencies...")
dependencies = {
    'tkinter': False,
    'PIL': False,
    'cv2': False,
    'ultralytics': False,
    'torch': False
}

try:
    import tkinter
    dependencies['tkinter'] = True
    print("✅ Tkinter available (version {})".format(tkinter.TkVersion))
except:
    print("❌ Tkinter not available")

try:
    from PIL import Image
    dependencies['PIL'] = True
    print("✅ PIL/Pillow available")
except:
    print("❌ PIL/Pillow not available")

try:
    import cv2
    dependencies['cv2'] = True
    print("✅ OpenCV available")
except:
    print("❌ OpenCV not available")

try:
    from ultralytics import YOLO
    dependencies['ultralytics'] = True
    print("✅ Ultralytics YOLO available")
except:
    print("❌ Ultralytics not available")

try:
    import torch
    dependencies['torch'] = True
    cuda_available = torch.cuda.is_available()
    print(f"✅ PyTorch available (CUDA: {cuda_available})")
except:
    print("❌ PyTorch not available")

print()
print("-"*60)

# Check model file
print("\nChecking model file...")
possible_paths = [
    Path("C:/Users/ASUS/runs/detect/train/weights/best.pt"),
    Path("runs/detect/train/weights/best.pt"),
    Path("best.pt"),
]

model_found = False
for path in possible_paths:
    if path.exists():
        print(f"✅ Model found: {path}")
        print(f"   Size: {path.stat().st_size / (1024*1024):.1f} MB")
        model_found = True
        break

if not model_found:
    print("❌ Model file not found in expected locations")
    print("   Please ensure training is complete")

print()
print("="*60)

# Summary
all_deps = all(dependencies.values())
if all_deps and model_found:
    print("✅ ALL CHECKS PASSED - App is ready to run!")
    print()
    print("To launch the app, run:")
    print("   python safety_vision_app.py")
    print("or double-click:")
    print("   run_app.bat")
else:
    print("⚠️  SOME CHECKS FAILED")
    print()
    if not all_deps:
        print("Missing dependencies:")
        for dep, available in dependencies.items():
            if not available:
                print(f"   - {dep}")
    if not model_found:
        print("   - Model file (best.pt)")

print("="*60)
