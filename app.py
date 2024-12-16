from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

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

        file_path = os.path.join(DOWNLOAD_FOLDER, f"{yt.title}.mp4")
        stream.download(output_path=DOWNLOAD_FOLDER, filename=f"{yt.title}.mp4")

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
