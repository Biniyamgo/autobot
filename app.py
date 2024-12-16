from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pytube import YouTube
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DOWNLOAD_FOLDER = "/tmp/downloads"  # Use a writable temporary folder for the server

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({"error": "URL is required"}), 400

    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

        if not stream:
            return jsonify({"error": "No suitable stream found"}), 404

        # Save the file locally
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{yt.title}.mp4")
        stream.download(output_path=DOWNLOAD_FOLDER, filename=f"{yt.title}.mp4")

        # Make sure the file is accessible
        os.chmod(file_path, 0o644)

        return jsonify({"download_url": f"/static/{yt.title}.mp4"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
