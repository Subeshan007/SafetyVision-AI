"""
SafetyVision AI - Space Station Safety Equipment Detection App
Duality AI Hackathon 2025 - Bonus Application

This app provides a user-friendly interface for detecting safety equipment
in space station images using our trained YOLOv8 model.
"""

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import cv2
from pathlib import Path
from ultralytics import YOLO
import threading
import os

class SafetyVisionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SafetyVision AI - Space Station Safety Monitor")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Model loading
        self.model = None
        self.model_path = self.find_model()
        self.current_image = None
        self.current_image_path = None
        
        # Class names
        self.class_names = [
            "OxygenTank", "NitrogenTank", "FirstAidBox", "FireAlarm",
            "SafetySwitchPanel", "EmergencyPhone", "FireExtinguisher"
        ]
        
        self.setup_ui()
        self.load_model_async()
    
    def find_model(self):
        """Find the best model file"""
        possible_paths = [
            Path("C:/Users/ASUS/runs/detect/train/weights/best.pt"),
            Path(__file__).parent / "runs" / "detect" / "train" / "weights" / "best.pt",
            Path(__file__).parent / "best.pt",
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        return None
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2d2d30', height=80)
        title_frame.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="🛡️ SafetyVision AI",
            font=('Arial', 28, 'bold'),
            bg='#2d2d30',
            fg='#00d4ff'
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Space Station Safety Equipment Detection System | Duality AI Challenge 2025",
            font=('Arial', 11),
            bg='#2d2d30',
            fg='#b0b0b0'
        )
        subtitle_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#1e1e1e')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Image display
        left_panel = tk.Frame(content_frame, bg='#2d2d30', relief='solid', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        image_title = tk.Label(
            left_panel,
            text="📸 Image Analysis",
            font=('Arial', 14, 'bold'),
            bg='#2d2d30',
            fg='white'
        )
        image_title.pack(pady=10)
        
        # Image canvas
        self.canvas = tk.Canvas(left_panel, bg='#1e1e1e', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Placeholder text
        self.placeholder_text = self.canvas.create_text(
            400, 300,
            text="No image loaded\n\nClick 'Select Image' to begin",
            font=('Arial', 16),
            fill='#666666',
            justify='center'
        )
        
        # Right panel - Controls and results
        right_panel = tk.Frame(content_frame, bg='#2d2d30', width=350, relief='solid', bd=2)
        right_panel.pack(side='right', fill='y')
        right_panel.pack_propagate(False)
        
        # Model status
        status_frame = tk.Frame(right_panel, bg='#2d2d30')
        status_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(
            status_frame,
            text="🤖 Model Status",
            font=('Arial', 12, 'bold'),
            bg='#2d2d30',
            fg='white'
        ).pack(anchor='w')
        
        self.status_label = tk.Label(
            status_frame,
            text="⏳ Loading model...",
            font=('Arial', 10),
            bg='#2d2d30',
            fg='#ffa500',
            wraplength=300,
            justify='left'
        )
        self.status_label.pack(anchor='w', pady=(5, 0))
        
        # Model performance
        perf_frame = tk.Frame(right_panel, bg='#353535', relief='solid', bd=1)
        perf_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            perf_frame,
            text="📊 Model Performance",
            font=('Arial', 11, 'bold'),
            bg='#353535',
            fg='white'
        ).pack(pady=8)
        
        metrics = [
            ("mAP@0.5", "77.64%", "#00ff00"),
            ("Precision", "88.97%", "#00d4ff"),
            ("Recall", "71.32%", "#ff9500")
        ]
        
        for metric, value, color in metrics:
            m_frame = tk.Frame(perf_frame, bg='#353535')
            m_frame.pack(fill='x', padx=15, pady=2)
            tk.Label(m_frame, text=f"{metric}:", font=('Arial', 9), bg='#353535', fg='#b0b0b0').pack(side='left')
            tk.Label(m_frame, text=value, font=('Arial', 9, 'bold'), bg='#353535', fg=color).pack(side='right')
        
        tk.Label(
            perf_frame,
            text="Competition-grade accuracy",
            font=('Arial', 8),
            bg='#353535',
            fg='#666666'
        ).pack(pady=(5, 8))
        
        # Control buttons
        button_frame = tk.Frame(right_panel, bg='#2d2d30')
        button_frame.pack(fill='x', padx=15, pady=15)
        
        self.select_btn = tk.Button(
            button_frame,
            text="📁 Select Image",
            command=self.select_image,
            font=('Arial', 12, 'bold'),
            bg='#0e639c',
            fg='white',
            activebackground='#1177bb',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            height=2
        )
        self.select_btn.pack(fill='x', pady=(0, 10))
        
        self.analyze_btn = tk.Button(
            button_frame,
            text="🔍 Analyze Image",
            command=self.analyze_image,
            font=('Arial', 12, 'bold'),
            bg='#107c10',
            fg='white',
            activebackground='#128c12',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            height=2,
            state='disabled'
        )
        self.analyze_btn.pack(fill='x', pady=(0, 10))
        
        self.save_btn = tk.Button(
            button_frame,
            text="💾 Save Results",
            command=self.save_results,
            font=('Arial', 11),
            bg='#5a5a5a',
            fg='white',
            activebackground='#6a6a6a',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            state='disabled'
        )
        self.save_btn.pack(fill='x')
        
        # Detection results
        results_frame = tk.Frame(right_panel, bg='#2d2d30')
        results_frame.pack(fill='both', expand=True, padx=15, pady=(10, 15))
        
        tk.Label(
            results_frame,
            text="🎯 Detection Results",
            font=('Arial', 12, 'bold'),
            bg='#2d2d30',
            fg='white'
        ).pack(anchor='w', pady=(0, 10))
        
        # Results text with scrollbar
        results_container = tk.Frame(results_frame, bg='#1e1e1e', relief='solid', bd=1)
        results_container.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(results_container)
        scrollbar.pack(side='right', fill='y')
        
        self.results_text = tk.Text(
            results_container,
            font=('Courier', 9),
            bg='#1e1e1e',
            fg='#d4d4d4',
            wrap='word',
            yscrollcommand=scrollbar.set,
            relief='flat',
            padx=10,
            pady=10
        )
        self.results_text.pack(fill='both', expand=True)
        scrollbar.config(command=self.results_text.yview)
        
        self.results_text.insert('1.0', "No analysis performed yet.\n\nSelect an image and click 'Analyze Image' to detect safety equipment.")
        self.results_text.config(state='disabled')
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='#2d2d30', height=40)
        footer_frame.pack(fill='x')
        
        tk.Label(
            footer_frame,
            text="Powered by YOLOv8 | Trained on Falcon Synthetic Data | Model: 77.64% mAP",
            font=('Arial', 9),
            bg='#2d2d30',
            fg='#888888'
        ).pack(pady=10)
    
    def load_model_async(self):
        """Load model in background thread"""
        def load():
            try:
                if self.model_path and self.model_path.exists():
                    self.model = YOLO(str(self.model_path))
                    self.root.after(0, lambda: self.status_label.config(
                        text=f"✅ Model loaded successfully\n{self.model_path.name}",
                        fg='#00ff00'
                    ))
                else:
                    self.root.after(0, lambda: self.status_label.config(
                        text="❌ Model file not found\nPlease train model first",
                        fg='#ff0000'
                    ))
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(
                    text=f"❌ Error loading model\n{str(e)}",
                    fg='#ff0000'
                ))
        
        threading.Thread(target=load, daemon=True).start()
    
    def select_image(self):
        """Open file dialog to select image"""
        file_path = filedialog.askopenfilename(
            title="Select Space Station Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, path):
        """Load and display image"""
        try:
            self.current_image_path = path
            image = Image.open(path)
            
            # Convert to RGB if necessary (fixes Google images with RGBA, grayscale, etc.)
            if image.mode != 'RGB':
                print(f"Converting image from {image.mode} to RGB")
                image = image.convert('RGB')
            
            # Resize to fit canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width, canvas_height = 750, 550
            
            image.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
            
            self.current_image = ImageTk.PhotoImage(image)
            
            # Clear canvas and display image
            self.canvas.delete('all')
            self.canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=self.current_image,
                anchor='center'
            )
            
            # Enable analyze button if model is loaded
            if self.model:
                self.analyze_btn.config(state='normal')
            
            # Update results
            self.results_text.config(state='normal')
            self.results_text.delete('1.0', 'end')
            self.results_text.insert('1.0', f"📷 Image loaded:\n{Path(path).name}\n\nReady for analysis.\nClick 'Analyze Image' to detect equipment.")
            self.results_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}\n\nTry saving the image as .jpg or .png first.")
    
    def analyze_image(self):
        """Analyze image with YOLO model"""
        if not self.model:
            messagebox.showwarning("Model Not Loaded", "Please wait for model to load.")
            return
        
        if not self.current_image_path:
            messagebox.showwarning("No Image", "Please select an image first.")
            return
        
        # Disable buttons during analysis
        self.analyze_btn.config(state='disabled', text="🔄 Analyzing...")
        self.root.update()
        
        try:
            # Ensure image is in correct format before detection
            temp_image = Image.open(self.current_image_path)
            if temp_image.mode != 'RGB':
                print(f"Converting {self.current_image_path} from {temp_image.mode} to RGB for detection")
                temp_image = temp_image.convert('RGB')
                # Save temporarily
                temp_path = Path(self.current_image_path).parent / f"temp_{Path(self.current_image_path).name}"
                temp_image.save(temp_path, 'PNG')
                detection_path = str(temp_path)
            else:
                detection_path = self.current_image_path
            
            # Run detection
            results = self.model.predict(
                detection_path,
                conf=0.5,
                verbose=False
            )
            
            # Clean up temp file if created
            if detection_path != self.current_image_path:
                try:
                    os.remove(detection_path)
                except:
                    pass
            
            result = results[0]
            
            # Get annotated image
            annotated = result.plot()
            annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(annotated_rgb)
            
            # Resize to fit canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width, canvas_height = 750, 550
            
            image.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
            self.current_image = ImageTk.PhotoImage(image)
            
            # Display annotated image
            self.canvas.delete('all')
            self.canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=self.current_image,
                anchor='center'
            )
            
            # Process detections
            detections = {}
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = self.class_names[cls_id]
                
                if class_name not in detections:
                    detections[class_name] = []
                detections[class_name].append(conf)
            
            # Update results text
            self.results_text.config(state='normal')
            self.results_text.delete('1.0', 'end')
            
            if detections:
                self.results_text.insert('end', "✅ DETECTION COMPLETE\n", 'title')
                self.results_text.insert('end', "="*40 + "\n\n")
                self.results_text.insert('end', f"📊 Total Objects: {len(result.boxes)}\n\n")
                
                self.results_text.insert('end', "🎯 Detected Equipment:\n")
                self.results_text.insert('end', "-"*40 + "\n\n")
                
                for idx, (class_name, confidences) in enumerate(sorted(detections.items()), 1):
                    count = len(confidences)
                    avg_conf = sum(confidences) / len(confidences) * 100
                    
                    self.results_text.insert('end', f"{idx}. {class_name}\n", 'class')
                    self.results_text.insert('end', f"   Count: {count}\n")
                    self.results_text.insert('end', f"   Avg Confidence: {avg_conf:.1f}%\n")
                    
                    if count > 1:
                        for i, conf in enumerate(confidences, 1):
                            self.results_text.insert('end', f"   #{i}: {conf*100:.1f}%\n", 'detail')
                    
                    self.results_text.insert('end', "\n")
                
                self.results_text.insert('end', "\n" + "="*40 + "\n")
                self.results_text.insert('end', "✅ Analysis successful!\n")
                self.results_text.insert('end', "💡 High confidence detections shown with green boxes\n")
                
            else:
                self.results_text.insert('end', "⚠️ NO EQUIPMENT DETECTED\n\n")
                self.results_text.insert('end', "No safety equipment found in this image.\n")
                self.results_text.insert('end', "This could mean:\n")
                self.results_text.insert('end', "• Image doesn't contain equipment\n")
                self.results_text.insert('end', "• Confidence threshold too high\n")
                self.results_text.insert('end', "• Equipment heavily occluded\n")
            
            # Configure text tags
            self.results_text.tag_config('title', foreground='#00ff00', font=('Courier', 10, 'bold'))
            self.results_text.tag_config('class', foreground='#00d4ff', font=('Courier', 9, 'bold'))
            self.results_text.tag_config('detail', foreground='#888888')
            
            self.results_text.config(state='disabled')
            
            # Enable save button
            self.save_btn.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Failed to analyze image:\n{str(e)}")
        
        finally:
            self.analyze_btn.config(state='normal', text="🔍 Analyze Image")
    
    def save_results(self):
        """Save annotated image"""
        if not self.current_image_path:
            return
        
        save_path = filedialog.asksaveasfilename(
            title="Save Annotated Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            initialfile=f"annotated_{Path(self.current_image_path).stem}.png"
        )
        
        if save_path:
            try:
                # Ensure image format compatibility
                temp_image = Image.open(self.current_image_path)
                if temp_image.mode != 'RGB':
                    temp_image = temp_image.convert('RGB')
                    temp_path = Path(self.current_image_path).parent / f"temp_save_{Path(self.current_image_path).name}"
                    temp_image.save(temp_path, 'PNG')
                    detection_path = str(temp_path)
                else:
                    detection_path = self.current_image_path
                
                # Run detection again to get clean annotated image
                results = self.model.predict(detection_path, conf=0.5, verbose=False)
                annotated = results[0].plot()
                cv2.imwrite(save_path, annotated)
                
                # Clean up temp file
                if detection_path != self.current_image_path:
                    try:
                        os.remove(detection_path)
                    except:
                        pass
                
                messagebox.showinfo("Success", f"Results saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save results:\n{str(e)}")

def main():
    root = tk.Tk()
    app = SafetyVisionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
