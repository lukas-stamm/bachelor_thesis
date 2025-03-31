from flask import Flask, jsonify, request, send_from_directory
import os
import json
import random
import csv

app = Flask(__name__, static_folder="../frontend", static_url_path="")

SUPABASE_BASE_URL = "https://ywseguqzfflegczeerzz.supabase.co/storage/v1/object/public/images/"  # <--- Passe das an
IMAGE_COUNT = 10
RESULTS_FILE = "ergebnisse.csv"

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route("/api/get_images")
def get_images():
    with open("images.json", "r") as f:
        all_images = json.load(f)

    selected = random.sample(all_images, min(IMAGE_COUNT, len(all_images)))

    images = [
        {
            "url": SUPABASE_BASE_URL + img,
            "name": img,
            "class": img.split("_")[0]
        } for img in selected
    ]

    return jsonify(images)

@app.route("/api/save_response", methods=["POST"])
def save_response():
    data = request.json
    with open(RESULTS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([data['class'], data['bild'], data['entscheidung'], data['alter'], data['zeit']])
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)