from flask import Flask, render_template, request, send_file, jsonify
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
        return jsonify({"error": "No URL"}), 400

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

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == "__main__":
    app.run()
