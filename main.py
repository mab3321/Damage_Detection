from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# Folder path where the images are located
IMAGE_FOLDER = r'data\body'

# Route to serve images


def find_string_index(lst, target):
    for idx, val in enumerate(lst):
        if target in val:
            return idx
    return False


@app.route('/images/<path:filename>')
def get_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

# API route to get image URLs and slider heading


@app.route('/api/data')
@cross_origin()
def get_slider_data():
    # Get all image filenames from the folder

    category = request.args.get('category')
    # Get Latest Folders
    directory = r'results'
    # Get all folders in the directory
    folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]

    # Sort the folders based on timestamps
    sorted_folders = sorted(folders, key=lambda x: x.rsplit('_')[-1])
    selected_folder = sorted_folders[-3:]
    index = find_string_index(selected_folder, category)
    if type(index) is int:
        IMAGE_FOLDER = rf'{directory}\{selected_folder[index]}'
    else:
        print("Folder not found")

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
