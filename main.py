import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np
import os
import json
from datetime import datetime, timedelta
import threading
import glob
from collections import defaultdict

class FaceTimelapseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Face Timelapse Creator")
        # Set to fullscreen mode
        self.root.state('zoomed')  # Windows fullscreen
        # Alternative for other platforms: self.root.attributes('-fullscreen', True)
        
        # Configuration
        self.photos_dir = "face_photos"
        self.config_file = "app_config.json"
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Camera setup
        self.cap = None
        self.camera_active = False
        self.face_detected = False
        self.face_centered = False
        self.reference_face_size = None
        
        # Create directories
        os.makedirs(self.photos_dir, exist_ok=True)
        
        # Load configuration
        self.load_config()
        
        # Setup blue theme
        self.setup_blue_theme()
        
        # Setup GUI
        self.setup_gui()
        
        # Setup keyboard bindings
        self.setup_keyboard_bindings()
        
        # Start camera
        self.start_camera()
        
    def setup_blue_theme(self):
        """Setup blue theme for the application"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure blue theme colors
        self.style.configure('TFrame', background="#337be6")
        self.style.configure('TLabel', background='#337be6', foreground='white')
        self.style.configure('TLabelFrame', background='#337be6', foreground='white')
        self.style.configure('TLabelFrame.Label', background='#337be6', foreground='white')
        self.style.configure('TButton', background='#337be6', foreground='white')
        self.style.configure('TEntry', fieldbackground='#337be6', foreground='white')
        self.style.configure('TCombobox', fieldbackground='#337be6', foreground='white')
        
        # Accent button style for primary actions
        self.style.configure('BlueAccent.TButton', 
                       background="#0065e0", 
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        # Delete button style
        self.style.configure('Delete.TButton',
                       background='#e74c3c',
                       foreground='white',
                       font=('Arial', 9))
        
        # Configure root window
        self.root.configure(bg="#69c3ff")
    
    def setup_keyboard_bindings(self):
        """Setup keyboard bindings for capture functionality"""
        self.root.bind('<KeyPress-space>', lambda e: self.capture_photo())
        self.root.bind('<KeyPress-Return>', lambda e: self.capture_photo())
        self.root.bind('<KeyPress-Delete>', lambda e: self.delete_selected_photo())
        self.root.bind('<KeyPress-Escape>', lambda e: self.toggle_fullscreen())
        
        # Make sure the root window can receive focus for key events
        self.root.focus_set()
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        current_state = self.root.state()
        if current_state == 'zoomed':
            self.root.state('normal')
            self.root.geometry("1600x900")  # Large windowed size
        else:
            self.root.state('zoomed')
    
    def load_config(self):
        """Load app configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.reference_face_size = config.get('reference_face_size')
        except:
            pass
    
    def save_config(self):
        """Save app configuration"""
        config = {'reference_face_size': self.reference_face_size}
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
    
    def setup_gui(self):
        """Setup the GUI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Camera and controls
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Camera frame
        camera_frame = ttk.LabelFrame(left_panel, text="Camera View")
        camera_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.camera_label = tk.Label(camera_frame, bg="#000000")
        self.camera_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(left_panel, text="Positioning Guide")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_text = tk.Text(status_frame, height=4, wrap=tk.WORD, 
                                  bg='#5590f6', fg='white', insertbackground='white')
        self.status_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Controls frame
        controls_frame = ttk.LabelFrame(left_panel, text="Controls")
        controls_frame.pack(fill=tk.X)
        
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.capture_btn = ttk.Button(button_frame, text="📸 Capture (Space/Enter)", 
                                     command=self.capture_photo, style="BlueAccent.TButton")
        self.capture_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.calibrate_btn = ttk.Button(button_frame, text="🎯 Set Reference Position", 
                                       command=self.set_reference_face)
        self.calibrate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.create_video_btn = ttk.Button(button_frame, text="🎬 Create Timelapse", 
                                          command=self.create_timelapse_dialog)
        self.create_video_btn.pack(side=tk.LEFT)
        
        # Keyboard shortcuts info
        shortcuts_frame = ttk.Frame(controls_frame)
        shortcuts_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        shortcuts_label = ttk.Label(shortcuts_frame, 
                                   text="⌨️ Keys: Space/Enter=Capture | Del=Delete | Esc=Exit Fullscreen",
                                   font=('Arial', 8))
        shortcuts_label.pack()
        
        # Right panel - Photo gallery
        right_panel = ttk.Frame(main_frame, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        gallery_frame = ttk.LabelFrame(right_panel, text="Photo Gallery")
        gallery_frame.pack(fill=tk.BOTH, expand=True)
        
        # Gallery controls
        gallery_controls = ttk.Frame(gallery_frame)
        gallery_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(gallery_controls, text="🔄 Refresh", 
                  command=self.refresh_gallery).pack(side=tk.LEFT)
        
        ttk.Button(gallery_controls, text="🗑️ Delete (Del)", 
                  command=self.delete_selected_photo, style="Delete.TButton").pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Button(gallery_controls, text="📂 Open Folder", 
                  command=self.open_photos_folder).pack(side=tk.RIGHT)
        
        # Gallery listbox with scrollbar
        gallery_list_frame = ttk.Frame(gallery_frame)
        gallery_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        self.gallery_listbox = tk.Listbox(gallery_list_frame, bg='#5590f6', fg='white', 
                                         selectbackground='#5590f6', selectforeground='white')
        gallery_scrollbar = ttk.Scrollbar(gallery_list_frame, orient=tk.VERTICAL, 
                                         command=self.gallery_listbox.yview)
        self.gallery_listbox.configure(yscrollcommand=gallery_scrollbar.set)
        
        self.gallery_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        gallery_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.gallery_listbox.bind('<Double-Button-1>', self.view_photo)
        self.gallery_listbox.bind('<<ListboxSelect>>', self.on_photo_select)
        
        # Photo preview
        self.preview_label = tk.Label(gallery_frame, text="Select a photo to preview", 
                                     bg="#5590f6", fg="white", height=8)
        self.preview_label.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Preview controls
        preview_controls = ttk.Frame(gallery_frame)
        preview_controls.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        ttk.Button(preview_controls, text="👁️ Full View", 
                  command=self.open_full_view).pack(side=tk.LEFT)
        
        ttk.Button(preview_controls, text="🗑️ Delete Selected", 
                  command=self.delete_selected_photo, style="Delete.TButton").pack(side=tk.RIGHT)
        
        # Statistics
        stats_frame = ttk.LabelFrame(right_panel, text="Statistics")
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.stats_text = tk.Text(stats_frame, height=6, wrap=tk.WORD,
                                 bg='#5590f6', fg='white', insertbackground='white')
        self.stats_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Advice Panel
        advice_frame = ttk.LabelFrame(right_panel, text="📝 Daily Timelapse Tips")
        advice_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.advice_text = tk.Text(advice_frame, height=8, wrap=tk.WORD,
                                  bg='#5590f6', fg='white', insertbackground='white',
                                  font=('Arial', 9))
        self.advice_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Initialize advice
        self.setup_advice_system()
        
        # Initial gallery load
        self.refresh_gallery()
        self.update_statistics()
        
    def start_camera(self):
        """Initialize camera with 16:9 aspect ratio"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open camera")
                return
            
            # Set camera resolution to 16:9 aspect ratio
            # Try different 16:9 resolutions, starting with highest quality
            resolutions_16_9 = [
                (1920, 1080),  # 1080p
                (1280, 720),   # 720p
                (854, 480),    # 480p
                (640, 360)     # 360p
            ]
            
            camera_set = False
            for width, height in resolutions_16_9:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                
                # Check if the resolution was actually set
                actual_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                actual_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                
                if abs(actual_width - width) < 50 and abs(actual_height - height) < 50:
                    self.camera_width = int(actual_width)
                    self.camera_height = int(actual_height)
                    camera_set = True
                    break
            
            if not camera_set:
                # Fallback to default resolution and crop to 16:9
                self.camera_width = 1280
                self.camera_height = 720
            
            self.camera_active = True
            self.update_camera()
        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to start camera: {str(e)}")
    
    def update_camera(self):
        """Update camera feed"""
        if not self.camera_active or not self.cap:
            return
            
        ret, frame = self.cap.read()
        if not ret:
            self.root.after(10, self.update_camera)
            return
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Ensure 16:9 aspect ratio by cropping if necessary
        h, w = frame.shape[:2]
        target_aspect = 16/9
        current_aspect = w/h
        
        if current_aspect > target_aspect:
            # Too wide, crop width
            new_width = int(h * target_aspect)
            start_x = (w - new_width) // 2
            frame = frame[:, start_x:start_x + new_width]
        elif current_aspect < target_aspect:
            # Too tall, crop height
            new_height = int(w / target_aspect)
            start_y = (h - new_height) // 2
            frame = frame[start_y:start_y + new_height, :]
        
        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Analyze face positioning
        self.analyze_face_position(frame, faces)
        
        # Draw guide overlay
        self.draw_guide_overlay(frame, faces)
        
        # Convert to PhotoImage and display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        
        # Scale for fullscreen display - maintain 16:9 aspect ratio
        # Use larger display size for fullscreen
        display_width = 1280
        display_height = 720
        frame_pil = frame_pil.resize((display_width, display_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(frame_pil)
        
        self.camera_label.configure(image=photo)
        self.camera_label.image = photo
        
        self.root.after(10, self.update_camera)
    
    def analyze_face_position(self, frame, faces):
        """Analyze face position and provide guidance"""
        h, w = frame.shape[:2]
        center_x, center_y = w // 2, h // 2
        
        if len(faces) == 0:
            self.face_detected = False
            self.face_centered = False
            self.update_status("❌ No face detected. Please position yourself in front of the camera.")
        elif len(faces) > 1:
            self.face_detected = True
            self.face_centered = False
            self.update_status("⚠️ Multiple faces detected. Please ensure only your face is visible.")
        else:
            self.face_detected = True
            x, y, fw, fh = faces[0]
            face_center_x = x + fw // 2
            face_center_y = y + fh // 2
            
            # Check centering
            center_threshold = 50
            x_centered = abs(face_center_x - center_x) < center_threshold
            y_centered = abs(face_center_y - center_y) < center_threshold
            
            # Check size consistency
            face_area = fw * fh
            size_ok = True
            size_guidance = ""
            
            if self.reference_face_size:
                size_diff = abs(face_area - self.reference_face_size) / self.reference_face_size
                if size_diff > 0.2:  # 20% tolerance
                    size_ok = False
                    if face_area < self.reference_face_size:
                        size_guidance = " Move closer to camera."
                    else:
                        size_guidance = " Move further from camera."
            
            self.face_centered = x_centered and y_centered and size_ok
            
            if self.face_centered:
                self.update_status("✅ Perfect position! Ready to capture.")
            else:
                guidance = "🎯 Adjust position: "
                if not x_centered:
                    guidance += f"Move {'left' if face_center_x > center_x else 'right'}. "
                if not y_centered:
                    guidance += f"Move {'down' if face_center_y > center_y else 'up'}. "
                guidance += size_guidance
                self.update_status(guidance)
    
    def draw_guide_overlay(self, frame, faces):
        """Draw positioning guides on frame"""
        h, w = frame.shape[:2]
        center_x, center_y = w // 2, h // 2
        
        # Draw center crosshair
        cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), (255, 255, 255), 2)
        cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), (255, 255, 255), 2)
        
        # Draw face guide circle
        guide_radius = 80
        cv2.circle(frame, (center_x, center_y), guide_radius, (0, 255, 255), 2)
        
        # Draw detected faces
        for (x, y, fw, fh) in faces:
            color = (0, 255, 0) if self.face_centered else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + fw, y + fh), color, 2)
            
            # Draw face center
            face_center_x = x + fw // 2
            face_center_y = y + fh // 2
            cv2.circle(frame, (face_center_x, face_center_y), 5, color, -1)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    def update_status(self, message):
        """Update status text"""
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, message)
    
    def set_reference_face(self):
        """Set reference face size for consistency"""
        if not self.face_detected:
            messagebox.showwarning("Warning", "No face detected. Please position yourself properly first.")
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 1:
            x, y, w, h = faces[0]
            self.reference_face_size = w * h
            self.save_config()
            messagebox.showinfo("Success", "Reference position set! Use this as your standard position for daily photos.")
        else:
            messagebox.showwarning("Warning", "Please ensure exactly one face is visible and centered.")
    
    def capture_photo(self):
        """Capture and save daily photo"""
        if not self.face_detected:
            messagebox.showwarning("Warning", "No face detected. Please position yourself properly.")
            return
        
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture frame")
            return
        
        frame = cv2.flip(frame, 1)
        
        # Ensure 16:9 aspect ratio for saved photo
        h, w = frame.shape[:2]
        target_aspect = 16/9
        current_aspect = w/h
        
        if current_aspect > target_aspect:
            # Too wide, crop width
            new_width = int(h * target_aspect)
            start_x = (w - new_width) // 2
            frame = frame[:, start_x:start_x + new_width]
        elif current_aspect < target_aspect:
            # Too tall, crop height
            new_height = int(w / target_aspect)
            start_y = (h - new_height) // 2
            frame = frame[start_y:start_y + new_height, :]
        
        # Add date overlay
        date_str = datetime.now().strftime("%d/%m/%Y")
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(date_str, font, 1, 2)[0]
        
        # Position date in bottom right
        x = frame.shape[1] - text_size[0] - 20
        y = frame.shape[0] - 20
        
        # Add background rectangle for better readability
        cv2.rectangle(frame, (x - 10, y - text_size[1] - 10), 
                     (x + text_size[0] + 10, y + 10), (0, 0, 0), -1)
        cv2.putText(frame, date_str, (x, y), font, 1, (255, 255, 255), 2)
        
        # Save photo
        filename = f"face_{datetime.now().strftime('%d%m%Y_%H%M%S')}.jpg"
        filepath = os.path.join(self.photos_dir, filename)
        
        cv2.imwrite(filepath, frame)
        
        messagebox.showinfo("Success", f"Photo saved as {filename}")
        self.refresh_gallery()
        self.update_statistics()
    
    def refresh_gallery(self):
        """Refresh photo gallery"""
        self.gallery_listbox.delete(0, tk.END)
        
        photo_files = glob.glob(os.path.join(self.photos_dir, "face_*.jpg"))
        photo_files.sort(reverse=True)  # Most recent first
        
        for photo_file in photo_files:
            basename = os.path.basename(photo_file)
            # Extract date from filename
            try:
                date_part = basename.split('_')[1].split('_')[0]
                date_obj = datetime.strptime(date_part, '%d%m%Y')
                display_name = f"{date_obj.strftime('%d/%m/%Y')} - {basename}"
            except:
                display_name = basename
            
            self.gallery_listbox.insert(tk.END, display_name)
    
    def on_photo_select(self, event):
        """Handle photo selection in gallery"""
        self.view_photo(event)
    
    def view_photo(self, event):
        """View selected photo with improved error handling"""
        selection = self.gallery_listbox.curselection()
        if not selection:
            return
        
        try:
            selected_item = self.gallery_listbox.get(selection[0])
            filename = selected_item.split(' - ')[-1]
            filepath = os.path.join(self.photos_dir, filename)
            
            if os.path.exists(filepath):
                # Load and resize image for preview
                img = Image.open(filepath)
                # Calculate aspect ratio preserving resize
                img_width, img_height = img.size
                max_width, max_height = 280, 200
                
                ratio = min(max_width/img_width, max_height/img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                self.preview_label.configure(image=photo, text="")
                self.preview_label.image = photo
            else:
                self.preview_label.configure(image="", text="Photo not found")
                self.preview_label.image = None
        except Exception as e:
            self.preview_label.configure(image="", text=f"Error loading photo: {str(e)}")
            self.preview_label.image = None
    
    def open_full_view(self):
        """Open selected photo in full view window"""
        selection = self.gallery_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a photo first.")
            return
        
        try:
            selected_item = self.gallery_listbox.get(selection[0])
            filename = selected_item.split(' - ')[-1]
            filepath = os.path.join(self.photos_dir, filename)
            
            if not os.path.exists(filepath):
                messagebox.showerror("Error", "Photo file not found.")
                return
            
            # Create full view window
            full_view = tk.Toplevel(self.root)
            full_view.title(f"Full View - {filename}")
            full_view.configure(bg='#5590f6')
            
            # Load image
            img = Image.open(filepath)
            
            # Calculate window size (max 80% of screen)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            max_width = int(screen_width * 0.8)
            max_height = int(screen_height * 0.8)
            
            img_width, img_height = img.size
            ratio = min(max_width/img_width, max_height/img_height, 1.0)
            
            if ratio < 1.0:
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            
            # Center window
            window_width, window_height = img.size
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            full_view.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # Display image
            label = tk.Label(full_view, image=photo, bg='#5590f6')
            label.pack()
            label.image = photo  # Keep reference
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open photo: {str(e)}")
    
    def delete_selected_photo(self):
        """Delete selected photo from gallery and filesystem"""
        selection = self.gallery_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a photo to delete.")
            return
        
        try:
            selected_item = self.gallery_listbox.get(selection[0])
            filename = selected_item.split(' - ')[-1]
            filepath = os.path.join(self.photos_dir, filename)
            
            # Confirm deletion
            result = messagebox.askyesno("Confirm Deletion", 
                                       f"Are you sure you want to delete '{filename}'?\n\nThis action cannot be undone.")
            
            if result:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    messagebox.showinfo("Success", f"Photo '{filename}' has been deleted.")
                    
                    # Clear preview if this photo was being previewed
                    self.preview_label.configure(image="", text="Select a photo to preview")
                    self.preview_label.image = None
                    
                    # Refresh gallery and statistics
                    self.refresh_gallery()
                    self.update_statistics()
                else:
                    messagebox.showerror("Error", "Photo file not found.")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete photo: {str(e)}")
    
    def open_photos_folder(self):
        """Open photos folder in file explorer"""
        import subprocess
        import platform
        
        if platform.system() == "Windows":
            subprocess.Popen(f'explorer "{os.path.abspath(self.photos_dir)}"')
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", os.path.abspath(self.photos_dir)])
        else:  # Linux
            subprocess.Popen(["xdg-open", os.path.abspath(self.photos_dir)])
    
    def update_statistics(self):
        """Update statistics display"""
        photo_files = glob.glob(os.path.join(self.photos_dir, "face_*.jpg"))
        
        if not photo_files:
            stats = "No photos captured yet.\nStart your daily photo journey!"
        else:
            # Group by date
            dates = defaultdict(int)
            for photo_file in photo_files:
                try:
                    basename = os.path.basename(photo_file)
                    date_part = basename.split('_')[1].split('_')[0]
                    date_obj = datetime.strptime(date_part, '%d%m%Y')
                    date_key = date_obj.strftime('%Y-%m-%d')
                    dates[date_key] += 1
                except:
                    continue
            
            total_photos = len(photo_files)
            unique_dates = len(dates)
            
            if dates:
                first_date = min(dates.keys())
                last_date = max(dates.keys())
                date_range = (datetime.strptime(last_date, '%Y-%m-%d') - 
                            datetime.strptime(first_date, '%Y-%m-%d')).days + 1
                consistency = f"{unique_dates}/{date_range} days"
            else:
                consistency = "0/0 days"
            
            stats = f"""Total Photos: {total_photos}
Unique Dates: {unique_dates}
Consistency: {consistency}
Latest: {max(dates.keys()) if dates else 'None'}
Ready for timelapse: {'Yes' if total_photos >= 2 else 'No'}"""
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
    
    def setup_advice_system(self):
        """Setup and display daily timelapse advice"""
        self.advice_tips = [
            "💡 CONSISTENCY TIP:\nTake photos at the same time each day for best results. Morning light is often most flattering.",
            
            "📷 LIGHTING TIP:\nPosition yourself facing a window or light source. Avoid harsh shadows by using soft, natural light.",
            
            "🎯 POSITIONING TIP:\nUse the reference position feature to maintain consistent face size and angle throughout your timelapse.",
            
            "👔 WARDROBE TIP:\nWear different colored clothes each day to see dramatic changes in your final timelapse video.",
            
            "⏰ TIMING TIP:\nBest times: 10AM-2PM for natural light. Avoid evening photos unless you have good indoor lighting.",
            
            "🖼️ FRAMING TIP:\nKeep your face centered in the frame. The 16:9 format creates cinematic results perfect for sharing.",
            
            "📅 COMMITMENT TIP:\nSet a daily phone reminder! Even 30 days of photos can create an amazing transformation video.",
            
            "🎬 VIDEO TIP:\nFor smooth timelapse, aim for 1 photo per day minimum. 60+ photos make excellent 10-second videos.",
            
            "✨ EXPRESSION TIP:\nTry different expressions occasionally - smile, serious, funny faces add personality to your timelapse!",
            
            "🔄 BACKUP TIP:\nRegularly create timelapse videos to preserve your progress. Photos can accumulate quickly!"
        ]
        
        self.current_tip_index = 0
        self.update_advice()
        
        # Auto-rotate tips every 15 seconds
        self.advice_timer()
    
    def update_advice(self):
        """Update the advice display"""
        if hasattr(self, 'advice_tips') and self.advice_tips:
            tip = self.advice_tips[self.current_tip_index]
            self.advice_text.delete(1.0, tk.END)
            self.advice_text.insert(1.0, tip)
    
    def advice_timer(self):
        """Timer to automatically cycle through advice tips"""
        if hasattr(self, 'advice_tips') and len(self.advice_tips) > 0:
            self.current_tip_index = (self.current_tip_index + 1) % len(self.advice_tips)
            self.update_advice()
        
        # Schedule next tip change (15 seconds)
        self.root.after(15000, self.advice_timer)
    
    def create_timelapse_dialog(self):
        """Show timelapse creation dialog"""
        photo_files = glob.glob(os.path.join(self.photos_dir, "face_*.jpg"))
        if len(photo_files) < 2:
            messagebox.showwarning("Warning", "Need at least 2 photos to create a timelapse.")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Timelapse Video")
        dialog.geometry("400x300")
        dialog.configure(bg='#5590f6')
        dialog.grab_set()
        
        # Date selection
        ttk.Label(dialog, text="Select Date Range:").pack(pady=10)
        
        date_frame = ttk.Frame(dialog)
        date_frame.pack(pady=5)
        
        ttk.Label(date_frame, text="From:").grid(row=0, column=0, padx=5)
        from_date = tk.StringVar()
        from_entry = ttk.Entry(date_frame, textvariable=from_date, width=12)
        from_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(date_frame, text="To:").grid(row=0, column=2, padx=5)
        to_date = tk.StringVar()
        to_entry = ttk.Entry(date_frame, textvariable=to_date, width=12)
        to_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(dialog, text="Format: DD/MM/YYYY").pack()
        
        # Video settings
        settings_frame = ttk.LabelFrame(dialog, text="Video Settings")
        settings_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(settings_frame, text="FPS:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        fps_var = tk.StringVar(value="5")
        ttk.Entry(settings_frame, textvariable=fps_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(settings_frame, text="Quality:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        quality_var = tk.StringVar(value="High")
        quality_combo = ttk.Combobox(settings_frame, textvariable=quality_var, 
                    values=["Low", "Medium", "High"], width=10)
        quality_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def create_video():
            try:
                from_str = from_date.get().strip()
                to_str = to_date.get().strip()
                
                if from_str and to_str:
                    from_dt = datetime.strptime(from_str, "%d/%m/%Y")
                    to_dt = datetime.strptime(to_str, "%d/%m/%Y")
                else:
                    from_dt = None
                    to_dt = None
                
                fps = int(fps_var.get())
                dialog.destroy()
                self.create_timelapse_video(from_dt, to_dt, fps, quality_var.get())
                
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use DD/MM/YYYY")
        
        ttk.Button(button_frame, text="Create Video", command=create_video, style='BlueAccent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Auto-fill with first and last photo dates
        photo_files.sort()
        if photo_files:
            try:
                first_file = os.path.basename(photo_files[0])
                last_file = os.path.basename(photo_files[-1])
                
                first_date_str = first_file.split('_')[1].split('_')[0]
                last_date_str = last_file.split('_')[1].split('_')[0]
                
                first_dt = datetime.strptime(first_date_str, '%d%m%Y')
                last_dt = datetime.strptime(last_date_str, '%d%m%Y')
                
                from_date.set(first_dt.strftime('%d/%m/%Y'))
                to_date.set(last_dt.strftime('%d/%m/%Y'))
            except:
                pass
    
    def create_timelapse_video(self, from_date, to_date, fps, quality):
        """Create timelapse video"""
        def create_video_thread():
            try:
                # Get photo files in date range
                photo_files = glob.glob(os.path.join(self.photos_dir, "face_*.jpg"))
                filtered_files = []
                
                for photo_file in photo_files:
                    try:
                        basename = os.path.basename(photo_file)
                        date_str = basename.split('_')[1].split('_')[0]
                        photo_date = datetime.strptime(date_str, '%d%m%Y')
                        
                        if from_date and to_date:
                            if from_date <= photo_date <= to_date:
                                filtered_files.append((photo_date, photo_file))
                        else:
                            filtered_files.append((photo_date, photo_file))
                    except:
                        continue
                
                if len(filtered_files) < 2:
                    messagebox.showerror("Error", "Not enough photos in date range.")
                    return
                
                # Sort by date
                filtered_files.sort(key=lambda x: x[0])
                
                # Create video filename
                start_date = filtered_files[0][0].strftime('%d%m%Y')
                end_date = filtered_files[-1][0].strftime('%d%m%Y')
                video_filename = f"face_timelapse_{start_date}_to_{end_date}.mp4"
                
                # Quality settings
                quality_settings = {
                    "Low": {"width": 640, "height": 480, "bitrate": "500k"},
                    "Medium": {"width": 1280, "height": 720, "bitrate": "2000k"},
                    "High": {"width": 1920, "height": 1080, "bitrate": "5000k"}
                }
                
                settings = quality_settings[quality]
                
                # Read first image to get dimensions
                first_img = cv2.imread(filtered_files[0][1])
                height, width = first_img.shape[:2]
                
                # Setup video writer
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))
                
                # Process each image
                for i, (date, photo_file) in enumerate(filtered_files):
                    img = cv2.imread(photo_file)
                    if img is not None:
                        out.write(img)
                    
                    # Update progress (this is simplified - in a real app you'd use a progress bar)
                    progress = (i + 1) / len(filtered_files) * 100
                    print(f"Progress: {progress:.1f}%")
                
                out.release()
                
                messagebox.showinfo("Success", f"Timelapse video created: {video_filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create video: {str(e)}")
        
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=create_video_thread)
        thread.daemon = True
        thread.start()
    
    def __del__(self):
        """Cleanup"""
        if self.cap:
            self.cap.release()

def main():
    root = tk.Tk()
    
    # Set blue theme as default
    style = ttk.Style()
    style.theme_use('clam')
    
    app = FaceTimelapseApp(root)
    
    def on_closing():
        app.camera_active = False
        if app.cap:
            app.cap.release()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
