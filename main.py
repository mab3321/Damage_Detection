from flask import Flask, jsonify, send_from_directory
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Folder path where the images are located
IMAGE_FOLDER = r'data\body'

# Route to serve images


@app.route('/images/<path:filename>')
@cross_origin()
def get_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

# API route to get image URLs


@app.route('/api/images')
@cross_origin()
def get_image_urls():
    # Get all image filenames from the folder
    image_files = os.listdir(IMAGE_FOLDER)
    image_urls = []

    # Create the URLs for the images
    for filename in image_files:
        image_urls.append(f'{IMAGE_FOLDER}\\' + filename)

    return jsonify(image_urls)


if __name__ == '__main__':
    app.run()
