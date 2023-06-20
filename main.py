from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Folder path where the images are located
IMAGE_FOLDER = r'data\body'

# Route to serve images


@app.route('/images/<path:filename>')
def get_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

# API route to get image URLs and slider heading


@app.route('/api/data')
def get_slider_data():
    # Get all image filenames from the folder

    category = request.args.get('category')
    if category == "body":
        IMAGE_FOLDER = rf'data\{category}'
    else:
        IMAGE_FOLDER = rf'data\underbody\{category}'
    image_files = os.listdir(IMAGE_FOLDER)
    image_urls = []

    # Create the URLs for the images
    for filename in image_files:
        image_urls.append(f'{IMAGE_FOLDER}\\' + filename)

    slider_data = {
        'heading': f"{category if category != 'oilLeakage' else 'oil Leakage'}",
        'image_urls': image_urls
    }

    return jsonify(slider_data)


if __name__ == '__main__':
    app.run(debug=True)
