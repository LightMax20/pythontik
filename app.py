from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download")
def download():
    url = request.args.get("url")

    if not url:
        return "No URL provided"

    filename = f"{uuid.uuid4()}.mp4"

    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': filename,
        'quiet': True,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(
            filename,
            as_attachment=True,
            download_name="tiktok_video.mp4"
        )

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == "__main__":
    app.run()
