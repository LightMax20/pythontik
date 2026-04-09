from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")

    filename = f"{uuid.uuid4()}.mp4"

    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': filename,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return str(e)

    finally:
        if os.path.exists(filename):
            os.remove(filename)
