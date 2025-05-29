# Audio Extractor Web App

A web application that allows users to extract audio from video files (MP4, WebM, MOV) by either uploading a file or providing a URL. The extracted audio is converted to MP3 format using ffmpeg.

## Features

- Drag and drop file upload
- Support for uploading via URL
- Progress tracking during file processing
- Download extracted audio in MP3 format
- Responsive design that works on desktop and mobile devices
- Support for large files up to 500MB

## Prerequisites

- Python 3.7+
- ffmpeg (must be installed on the system)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd en-accent-detector
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install ffmpeg on your system:
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Upload a video file**:
   - Click the "Upload File" tab
   - Drag and drop a video file or click to browse
   - Supported formats: MP4, WebM, MOV (up to 500MB)

2. **Or provide a video URL**:
   - Click the "From URL" tab
   - Paste the URL of the video file
   - Click "Extract Audio"

3. **Download the audio**:
   - Once processing is complete, click the "Download MP3" button
   - The audio will be saved in MP3 format

## Project Structure

```
.
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── static/              # Static files (CSS, JS, uploads)
│   └── uploads/         # Directory for uploaded files
└── templates/           # HTML templates
    └── index.html       # Main application page
```

## Deployment

This application can be deployed to any platform that supports Python web applications. Some options include:

- **Vercel** (with serverless functions)
- **Heroku**
- **PythonAnywhere**
- **Google App Engine**
- **AWS Elastic Beanstalk**

### Vercel Deployment

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyourusername%2Faudio-extractor&demo-title=Audio%20Extractor&demo-description=Extract%20audio%20from%20videos%20online&demo-url=https%3A%2F%2Faudio-extractor.vercel.app%2F)

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Run with Gunicorn
```
gunicorn -w 4 -b 127.0.0.1:8000 wsgi:app
```