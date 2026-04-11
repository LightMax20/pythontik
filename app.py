from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


# 🎥 PREVIEW
@app.route("/preview")
def preview():
    url = request.args.get("url")

    ydl_opts = {'quiet': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail")
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# 📥 DOWNLOAD (HD / MP3)
@app.route("/download")
def download():
    url = request.args.get("url")
    mode = request.args.get("mode", "video")

    filename = f"{uuid.uuid4()}"

    if mode == "mp3":
        filename += ".mp3"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'quiet': True
        }
    else:
        filename += ".mp4"
        ydl_opts = {
            'format': 'mp4/best',
            'outtmpl': filename,
            'quiet': True
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(
            filename,
            as_attachment=True,
            download_name="tiktok_download"
        )

    except Exception as e:
        return str(e)

    finally:
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
