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
    file_type = request.args.get("type", "video")

    filename = "output"

    if file_type == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
        filename += ".mp3"
    else:
        ydl_opts = {
            'format': 'mp4/best',
            'outtmpl': filename
        }
        filename += ".mp4"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return str(e)

    finally:
        if os.path.exists(filename):
            os.remove(filename)

