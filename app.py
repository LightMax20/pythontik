from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import uuid
import os
import time

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


# 🎥 PREVIEW
@app.route("/preview")
def preview():
    url = request.args.get("url")

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail")
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# 📥 DOWNLOAD (WITH RETRY + FIXES)
@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    mode = request.form.get("mode")
    quality = request.form.get("quality", "best")

    file_id = str(uuid.uuid4())

    for attempt in range(3):  # 🔁 retry system
        try:
            # 🎵 MP3
            if mode == "mp3":
                filename = f"{file_id}.mp3"

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f"{DOWNLOAD_FOLDER}/{file_id}.%(ext)s",
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                    }],
                    'quiet': True
                }

            # 🎬 VIDEO
            else:
                filename = f"{file_id}.mp4"

                fmt = "best"
                if quality == "720":
                    fmt = "bestvideo[height<=720]+bestaudio/best || best"
                elif quality == "480":
                    fmt = "bestvideo[height<=480]+bestaudio/best || best"

                ydl_opts = {
                    'format': fmt,
                    'outtmpl': f"{DOWNLOAD_FOLDER}/{filename}",
                    'quiet': True
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return jsonify({"file": filename})

        except Exception as e:
            if attempt == 2:
                return jsonify({"error": str(e)})
            time.sleep(1)


# 📤 FILE DOWNLOAD
@app.route("/file/<name>")
def get_file(name):
    path = os.path.join(DOWNLOAD_FOLDER, name)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
