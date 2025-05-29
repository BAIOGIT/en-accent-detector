# English Accent Evaluation Tool

A Flask web application that extracts audio from videos and detects English accents using AI. Supports both local file uploads and URL downloads (Loom videos and direct video URLs).

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🎬 **Video Support**: Upload video files or provide URLs (Loom, direct video links)
- 🎵 **Audio Extraction**: Extract high-quality WAV audio using FFmpeg
- 🗣️ **Accent Detection**: Detect English accents using AI models
- 🔄 **Dual Inference**: Support for both local models and Hugging Face Inference API
- 📱 **Modern UI**: Clean, responsive web interface with drag-and-drop
- 🐳 **Docker Ready**: Containerized for easy deployment

## 🚀 Supported Formats

### Video Formats
- MP4, MOV, AVI, MKV, WebM, M4V, 3GP

### URL Types
- **Loom Videos**: `https://www.loom.com/share/video-id`
- **Direct URLs**: `https://example.com/video.mp4`

## 📦 Installation

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/en-accent-detector.git
   cd en-accent-detector
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg**:
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

5. **Configure environment**:
   ```bash
   cp .env.template .env
   # Edit .env with your settings
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

Visit `http://localhost:5000` in your browser.

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_INFERENCE_API` | `false` | Use Hugging Face Inference API instead of local model |
| `HF_API_TOKEN` | `` | Your Hugging Face API token (required for API mode) |
| `FLASK_ENV` | `development` | Flask environment (`development` or `production`) |

### Model Configuration

The app uses the `dima806/english_accents_classification` model for accent detection.

**Local Mode**: Downloads and runs the model locally (requires ~1GB RAM to load, ~3GB RAM for inference)
**API Mode**: Uses Hugging Face Inference API (requires API token)

## 🔧 API Endpoints

### Web Interface
- `GET /` - Main application interface
- `GET /health` - Health check endpoint

### API Endpoints
- `POST /upload` - Upload video file for processing
- `POST /download_url` - Process video from URL
- `GET /download/<audio_id>` - Download extracted audio file
- `GET /config` - Get current configuration

### Example API Usage

```bash
# Upload file
curl -X POST -F "file=@video.mp4" http://localhost:5000/upload

# Process URL
curl -X POST -H "Content-Type: application/json" \
  -d '{"url":"https://www.loom.com/share/video-id"}' \
  http://localhost:5000/download_url
```

## 🛠️ Development

### Project Structure

```
en-accent-detector/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env.template         # Environment template
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Temporary upload folder
├── output/               # Audio output folder
└── README.md            # This file
```

### Adding New Features

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-feature`
3. **Make changes and test**
4. **Submit pull request**

## 🔍 Troubleshooting

### Common Issues

**FFmpeg not found**:
```bash
# Install FFmpeg
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

**Model loading fails**:
- Check internet connection for model download
- Verify Hugging Face token if using API mode
- Ensure sufficient RAM (1GB+) for local mode

**Video processing errors**:
- Verify video file has audio tracks
- Check supported formats (MP4, MOV, AVI, MKV, WebM)
- Ensure file size is under 500MB

**Loom URL issues**:
- Verify URL format: `https://www.loom.com/share/video-id`
- Check if video is publicly accessible
- Some Loom videos may require authentication

### Debug Mode

Enable debug logging:
```bash
export FLASK_ENV=development
python app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the accent classification model
- [FFmpeg](https://ffmpeg.org/) for audio/video processing
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Loom](https://www.loom.com/) for video hosting

---