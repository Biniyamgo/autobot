from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({"error": "URL is required"}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = [{
                "format_id": f["format_id"],
                "format": f["format"],
                "url": f["url"]
            } for f in info.get('formats', [])]

            return jsonify({"title": info.get('title'), "formats": formats})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
