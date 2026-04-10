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

    if not url:
        return "No URL provided"

    filename = f"{uuid.uuid4()}.mp4"

    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': filename,
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # IMPORTANT: no as_attachment → opens in browser
        return send_file(filename, mimetype="video/mp4")

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == "__main__":
    app.run()
