# 📸 Daily Face Timelapse Creator

**Version 1.0.0** - Released August 24, 2025

Create stunning daily face timelapse videos with this professional, easy-to-use application. Track your transformation over days, weeks, months, or years with consistent, high-quality photos automatically processed into beautiful timelapse videos.

![App Preview](https://img.shields.io/badge/Version-1.0.0-blue) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-brightgreen) ![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Key Features

### 📷 **Smart Camera System**
- **16:9 Cinematic Format** - Professional widescreen aspect ratio for stunning videos
- **Automatic Face Detection** - AI-powered face recognition ensures perfect positioning
- **Real-time Positioning Guide** - Live feedback for consistent photo alignment
- **Multiple Resolution Support** - Automatically selects best available quality (up to 1080p)
- **Mirror Mode** - Flipped camera view for natural selfie experience

### 🎯 **Intelligent Positioning**
- **Reference Position Calibration** - Set your perfect position once, maintain it forever
- **Visual Guide Overlay** - On-screen crosshairs and guides for precise alignment
- **Smart Size Detection** - Automatic distance guidance (move closer/further)
- **Centering Assistance** - Real-time directional feedback (left/right/up/down)
- **Consistency Tracking** - Maintains face size and position across all photos

### 🖥️ **Modern Interface**
- **Fullscreen Experience** - Immersive fullscreen mode for distraction-free use
- **Beautiful Blue Theme** - Professional, easy-on-the-eyes color scheme
- **Real-time Preview** - Live camera feed with positioning guides
- **Intuitive Controls** - Clean, modern button layout with emoji icons
- **Responsive Design** - Scales perfectly to any screen size

### ⌨️ **Keyboard Shortcuts**
- **Space/Enter** - Capture photo instantly
- **Delete** - Remove selected photos
- **Escape** - Toggle fullscreen mode
- **Focus-aware** - Shortcuts work anywhere in the app

### 📱 **Photo Management**
- **Auto-organized Gallery** - Photos sorted by date with smart naming
- **Instant Preview** - Click any photo for immediate preview
- **Full-screen Viewer** - Detailed photo inspection with zoom
- **Batch Operations** - Select and manage multiple photos
- **Safe Deletion** - Confirmation dialogs prevent accidental loss
- **Folder Integration** - Direct access to photo storage location

### 🎬 **Video Creation**
- **Professional Timelapse Generator** - Create smooth, high-quality videos
- **Flexible Date Ranges** - Select specific time periods for videos
- **Multiple Quality Options** - Low/Medium/High quality settings
- **Custom Frame Rates** - Adjustable FPS for different effects
- **Smart Processing** - Automatic image alignment and optimization
- **Multiple Formats** - MP4 output compatible with all platforms

### 📊 **Analytics & Tracking**
- **Progress Statistics** - Track total photos, unique dates, consistency
- **Visual Progress Indicators** - See your timelapse journey at a glance
- **Streak Tracking** - Monitor your daily photo consistency
- **Timeline Overview** - Visual representation of your photo history

### 💡 **Built-in Advice System**
- **10 Professional Tips** - Expert guidance for better timelapse photography
- **Auto-rotating Advice** - New tip every 15 seconds
- **Comprehensive Coverage** - Lighting, timing, positioning, and creative tips
- **Beginner-friendly** - Perfect for first-time timelapse creators

### ⚡ **Performance & Reliability**
- **Threaded Processing** - Non-blocking video creation
- **Memory Efficient** - Optimized for long-term daily use
- **Auto-save Configuration** - Remembers your settings
- **Error Recovery** - Graceful handling of camera/file issues
- **Cross-platform** - Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Requirements
- **Python 3.8+**
- **Webcam** (built-in or USB)
- **Storage space** (approx. 2-5MB per photo)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nhattan86/Daily-Face-Timelapse-App.git
   cd Daily-Face-Timelapse-App
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install opencv-python pillow numpy tkinter
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

### First Time Setup

1. **Launch the app** - Automatically opens in fullscreen mode
2. **Position yourself** - Center your face using the on-screen guides
3. **Set reference position** - Click "🎯 Set Reference Position" for consistency
4. **Take your first photo** - Press Space, Enter, or click the capture button
5. **Start your journey** - Take a photo every day at the same time!

## 📋 Usage Guide

### Daily Photo Routine
1. **Launch the app** at your preferred time each day
2. **Position yourself** using the visual guides and status feedback
3. **Wait for green confirmation** - "✅ Perfect position! Ready to capture."
4. **Capture photo** using Space, Enter, or the capture button
5. **Review your photo** in the gallery preview

### Creating Timelapse Videos
1. **Take at least 2 photos** (recommend 30+ for best results)
2. **Click "🎬 Create Timelapse"**
3. **Select date range** or use all photos
4. **Choose quality and frame rate**
5. **Click "Create Video"** and wait for processing
6. **Find your video** in the app directory

### Photo Management
- **View photos** - Click any photo in the gallery
- **Full screen view** - Click "👁️ Full View" for detailed inspection
- **Delete photos** - Select photo and press Delete or click delete button
- **Browse folder** - Click "📂 Open Folder" to access photos directly

## 🎨 Interface Overview

### Main Interface
- **Left Panel**: Live camera view with positioning guides
- **Right Panel**: Photo gallery, statistics, and advice tips
- **Bottom Controls**: Capture, calibration, and timelapse creation buttons

### Color Scheme
- **Primary Blue**: `#4a6fa5` - Main backgrounds and frames
- **Secondary Blue**: `#6b8cc4` - Text areas and controls
- **Accent Blue**: `#7ba7db` - Highlights and selections
- **Action Red**: `#e74c3c` - Delete buttons and warnings

## 🛠️ Technical Specifications

### Image Processing
- **Format**: JPEG with date overlay
- **Aspect Ratio**: 16:9 (cinematic format)
- **Resolution**: Up to 1920x1080 (auto-selected based on camera)
- **Compression**: Optimized for storage efficiency

### Video Output
- **Format**: MP4 (H.264)
- **Aspect Ratio**: 16:9
- **Quality Options**:
  - Low: 640x360, 500k bitrate
  - Medium: 1280x720, 2000k bitrate  
  - High: 1920x1080, 5000k bitrate
- **Frame Rates**: 1-30 FPS (5 FPS recommended)

### File Management
- **Photo Storage**: `face_photos/` directory
- **Configuration**: `app_config.json` for settings
- **Naming Convention**: `face_DDMMYYYY_HHMMSS.jpg`
- **Video Output**: `face_timelapse_DDMMYYYY_to_DDMMYYYY.mp4`

## 🔧 Configuration

The app automatically saves your preferences in `app_config.json`:

```json
{
  "reference_face_size": 15840
}
```

### Customizable Settings
- **Reference face size** - Automatically saved when calibrated
- **Photo directory** - Modify `photos_dir` in code
- **Camera index** - Change for external cameras
- **Quality presets** - Adjust video encoding settings

## 🎯 Tips for Best Results

### 📷 **Photography Tips**
- **Consistent timing** - Same time each day for consistent lighting
- **Good lighting** - Face a window or use soft indoor lighting
- **Stable setup** - Use the same chair/position daily
- **Varied clothing** - Different colors create visual interest

### 🎬 **Timelapse Tips**
- **Minimum photos** - 30+ photos for smooth video
- **Frame rate** - 5 FPS works well for daily photos
- **Video length** - 1 photo per day = ~2 seconds per month at 5 FPS
- **Quality** - Use High quality for sharing, Medium for quick previews

## 🐛 Troubleshooting

### Common Issues

**Camera not detected:**
- Check if camera is being used by another app
- Try different camera index in code (0, 1, 2...)
- Restart the application

**Poor photo quality:**
- Ensure good lighting conditions
- Clean camera lens
- Check camera resolution settings

**Video creation fails:**
- Ensure at least 2 photos exist
- Check available disk space
- Close other video applications

**App crashes on startup:**
- Verify all dependencies are installed
- Check Python version (3.8+ required)
- Delete `app_config.json` to reset settings

## 📝 Version History

### Version 1.0.0 (August 24, 2025)
- 🎉 **Initial Release**
- ✅ Complete face detection and positioning system
- ✅ 16:9 cinematic camera format
- ✅ Fullscreen interface with blue theme
- ✅ Comprehensive keyboard shortcuts
- ✅ Smart photo gallery with preview
- ✅ Professional timelapse video creation
- ✅ Built-in advice system with 10 expert tips
- ✅ Real-time statistics and progress tracking
- ✅ Cross-platform compatibility

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenCV** - Computer vision and camera handling
- **Pillow (PIL)** - Image processing and manipulation
- **Tkinter** - Cross-platform GUI framework
- **NumPy** - Numerical computations

## 📞 Support

For questions, issues, or feature requests:
- **GitHub Issues**: [Create an issue](https://github.com/nhattan86/Daily-Face-Timelapse-App/issues)

---

**Start your transformation journey today! 📸✨**

> "A year from now, you'll wish you had started today." - Create your daily face timelapse and document your amazing transformation journey!