#!/usr/bin/env python

import logging
import os
from flask import Flask, request, jsonify, abort, send_file
from pathlib import Path

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

FILE_SECRET = os.environ.get("FILE_SECRET")

IMAGE_DIR = Path("images")
IMAGE_DIR.mkdir(exist_ok=True)


@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "message": "Use /image/<file_name>"
    })


def validate_secret():
    secret = request.headers.get("X-Image-Secret")
    if secret != FILE_SECRET:
        logging.warning("Invalid secret")
        abort(403)


@app.route('/image/<file_name>', methods=['GET'])
def get_image(file_name):
    validate_secret()

    file_path = IMAGE_DIR / f"{file_name}.png"

    if not file_path.exists():
        abort(404)

    return send_file(file_path, mimetype='image/png')


@app.route('/image/<file_name>', methods=['POST'])
def save_image(file_name):
    validate_secret()

    file_path = IMAGE_DIR / f"{file_name}.png"

    if not request.data:
        return jsonify({"error": "No data provided"}), 400

    with open(file_path, 'wb') as f:
        f.write(request.data)

    return jsonify({"status": "saved"}), 201


if __name__ == "__main__":
    port = int(os.environ.get("APP_PORT", 5000))
    app.run(host="0.0.0.0", port=port)