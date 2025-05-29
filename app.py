from flask import Flask, render_template, request, jsonify, send_file
import os
import ffmpeg
from werkzeug.utils import secure_filename
import uuid
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
import requests
from transformers import pipeline
import librosa
from urllib.parse import urlparse

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/output'

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Initialize the accent classifier pipeline
print("Loading accent classifier model...")
try:
    accent_classifier = pipeline("audio-classification", model="dima806/english_accents_classification")
    print("Accent classifier loaded successfully!")
except Exception as e:
    print(f"Error loading accent classifier: {e}")
    accent_classifier = None

def is_loom_video_url(url):
    """Check if URL is a Loom video URL"""
    loom_domain = 'www.loom.com'
    trimmed_url = url.strip()
    return trimmed_url.startswith('https://') and loom_domain in trimmed_url

def is_direct_video_url(url):
    """Check if URL is a direct video file URL"""
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.m4v', '.3gp']
    parsed_url = urlparse(url.lower())
    path = parsed_url.path
    return any(path.endswith(ext) for ext in video_extensions)

def get_loom_video_id(video_url):
    """Extract video ID from Loom URL"""
    return video_url.rstrip('/').split('/')[-1].split('?')[0]

def fetch_loom_download_url(video_id):
    """Fetch the direct download URL for a Loom video"""
    url = f"https://www.loom.com/api/campaigns/sessions/{video_id}/transcoded-url"
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json; charset=utf-8',
        'origin': 'https://www.loom.com',
        'referer': f'https://www.loom.com/share/{video_id}',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'pragma': 'no-cache',
        'x-content-type-options': 'nosniff',
        'x-frame-options': 'DENY',
    }
    
    data = json.dumps({}).encode('utf-8')
    
    request_obj = urllib.request.Request(
        url=url,
        data=data,
        headers=headers,
        method="POST",
    )
    
    try:
        response = urllib.request.urlopen(request_obj)
        body = response.read()
        content = json.loads(body.decode("utf-8"))
        video_url = content.get("url")
        if video_url:
            return {'success': True, 'data': video_url}
        else:
            return {'success': False, 'message': 'No video URL found in response'}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else 'No error details'
        return {'success': False, 'message': f'HTTP Error {e.code}: {error_body}'}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def download_video_from_url(video_url, unique_id):
    """Download video from direct URL"""
    try:
        # Get file extension from URL
        parsed_url = urlparse(video_url)
        path = parsed_url.path
        extension = '.mp4'  # default
        if '.' in path:
            extension = '.' + path.split('.')[-1].lower()
        
        filename = f"{unique_id}{extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        print(f"Downloading video from: {video_url}")
        with requests.get(video_url, stream=True, headers=headers, timeout=30) as r:
            r.raise_for_status()
            
            # Check if the content is actually a video
            content_type = r.headers.get('content-type', '').lower()
            if not (content_type.startswith('video/') or content_type.startswith('application/octet-stream')):
                raise Exception(f"URL does not point to a video file. Content-Type: {content_type}")
            
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"Video downloaded successfully to: {file_path}")
        return file_path
    except Exception as e:
        raise Exception(f'Error downloading video: {str(e)}')

def extract_audio(video_path, unique_id):
    """Extract audio from video file using ffmpeg-python"""
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{unique_id}.wav")
    
    try:
        # First, probe the video to check if it has audio streams
        probe = ffmpeg.probe(video_path)
        audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
        
        if not audio_streams:
            raise Exception("Video file contains no audio streams")
        
        # Extract audio with proper sampling rate for the model (16kHz)
        (
            ffmpeg
            .input(video_path)
            .output(output_path, 
                   vn=None,  # no video
                   acodec='pcm_s16le',
                   ar=16000,  # 16kHz sampling rate for the model
                   ac=1)      # mono audio
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        raise Exception(f"FFmpeg error: {e.stderr.decode()}")
    
    return output_path

def detect_accent(audio_path):
    """Detect English accent from audio file"""
    if not accent_classifier:
        return {'error': 'Accent classifier not available'}
    
    try:
        # Load audio file with librosa (the model expects 16kHz mono)
        audio, sample_rate = librosa.load(audio_path, sr=16000, mono=True)
        
        # Run inference
        results = accent_classifier(audio)

        print(f"Accent detection results: {results}")
        
        # Format results for better display
        formatted_results = []
        for result in results:
            accent = result['label']
            confidence = result['score']
            formatted_results.append({
                'accent': accent,
                'confidence': round(confidence * 100, 2)
            })
        
        return {
            'success': True,
            'results': formatted_results,
            'top_accent': formatted_results[0]['accent'],
            'top_confidence': formatted_results[0]['confidence']
        }
        
    except Exception as e:
        return {'error': f'Error detecting accent: {str(e)}'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if it's a valid video file
        allowed_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            return jsonify({'error': 'Please upload a valid video file (MP4, MOV, AVI, MKV, WebM)'}), 400
        
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
        file.save(file_path)
        
        # Extract audio
        audio_path = extract_audio(file_path, unique_id)
        
        # Detect accent
        accent_result = detect_accent(audio_path)
        
        # Clean up video file
        os.remove(file_path)
        
        response_data = {
            'success': True,
            'audio_id': unique_id,
            'message': 'Audio extracted successfully from uploaded file'
        }
        
        # Add accent detection results
        if 'error' in accent_result:
            response_data['accent_error'] = accent_result['error']
        else:
            response_data['accent_detection'] = accent_result
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_url', methods=['POST'])
def download_from_url():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Basic URL validation
        if not (url.startswith('http://') or url.startswith('https://')):
            return jsonify({'error': 'Please provide a valid HTTP/HTTPS URL'}), 400
        
        unique_id = str(uuid.uuid4())
        
        # Check if it's a Loom URL
        if is_loom_video_url(url):
            print("Processing Loom URL...")
            # Handle Loom video
            video_id = get_loom_video_id(url)
            
            # Get the direct download URL
            url_response = fetch_loom_download_url(video_id)
            if not url_response['success']:
                return jsonify({'error': f"Failed to get Loom video URL: {url_response['message']}"}), 400
            
            # Download the video
            video_path = download_video_from_url(url_response['data'], unique_id)
            
        # Check if it's a direct video URL
        elif is_direct_video_url(url):
            print("Processing direct video URL...")
            # Download directly
            video_path = download_video_from_url(url, unique_id)
            
        else:
            return jsonify({'error': 'Please provide a valid Loom URL or direct video file URL (MP4, MOV, AVI, MKV, WebM)'}), 400
        
        # Extract audio
        audio_path = extract_audio(video_path, unique_id)
        
        # Detect accent
        accent_result = detect_accent(audio_path)
        
        # Clean up video file
        os.remove(video_path)
        
        response_data = {
            'success': True,
            'audio_id': unique_id,
            'message': 'Audio extracted successfully from video URL'
        }
        
        # Add accent detection results
        if 'error' in accent_result:
            response_data['accent_error'] = accent_result['error']
        else:
            response_data['accent_detection'] = accent_result
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<audio_id>')
def download_audio(audio_id):
    try:
        audio_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{audio_id}.wav")
        if os.path.exists(audio_path):
            return send_file(audio_path, as_attachment=True, download_name=f"extracted_audio_{audio_id}.wav")
        else:
            return jsonify({'error': 'Audio file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/about')
def about():
    return 'Audio Extractor with English Accent Detection - Extract audio from video files, Loom URLs, or direct video URLs and detect English accents'

if __name__ == '__main__':
    app.run(debug=True)