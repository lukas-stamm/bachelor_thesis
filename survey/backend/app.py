# === backend/app.py ===
from flask import Flask, jsonify, request, send_from_directory
import os
import json
import random
import requests

app = Flask(__name__, static_folder="../frontend", static_url_path="")

SUPABASE_BASE_URL = "https://ywseguqzfflegczeerzz.supabase.co/storage/v1/object/public/images/"  # Replace with your Supabase project URL
SUPABASE_API_URL = "https://ywseguqzfflegczeerzz.supabase.co/rest/v1/ergebnisse"  # Replace with your Supabase REST endpoint
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl3c2VndXF6ZmZsZWdjemVlcnp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM0NjA0ODEsImV4cCI6MjA1OTAzNjQ4MX0.E_hVa1nyxilO-BYGYAXqOiYBuCh1LlEHPonRmVNtatc"  # Replace with your Supabase API key
IMAGE_COUNT = 10

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

    payload = {
        "class": data["class"],
        "image_id": data["bild"],
        "choice": data["entscheidung"],
        "age": data["alter"],
        "time": data["zeit"]
    }

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    res = requests.post(SUPABASE_API_URL, headers=headers, json=payload)

    if res.status_code == 201 or res.status_code == 204:
        return jsonify({"status": "ok"})
    else:
        print("❌ Fehler beim Speichern in Supabase:", res.status_code, res.text)
        return jsonify({"status": "error", "details": res.text}), 500

if __name__ == '__main__':
    app.run(debug=True)