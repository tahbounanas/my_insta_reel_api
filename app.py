from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

def extract_data_from_insta_reel(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        user = info.get("uploader_id")  # Proper @username
        if user:
            user = "@" + user

        reel_caption = info.get("description") or "Enjoy this reel"
        reel_caption = reel_caption.replace('\n', ' ').replace(';', ',')

        reel_link = info.get("url")

    return {
        "username": user,
        "video_url": reel_link,
        "caption": reel_caption
    }

@app.route("/")
def home():
    return "Instagram Reel Extractor API is running."

@app.route("/extract")
def extract():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Please provide a URL parameter, e.g., /extract?url=https://..."})
    
    try:
        result = extract_data_from_insta_reel(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
