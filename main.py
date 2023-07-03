from flask import Flask, jsonify, send_from_directory, request, render_template
from flask_cors import CORS, cross_origin
import os
import shutil
from work import Worker
from PIL import Image
from pathlib import Path
import io
from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import locale
locale.getpreferredencoding()
locale.getpreferredencoding = lambda: "UTF-8"


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


@app.route('/api/detect')
@cross_origin()
def detect():
    try:
        Worker()
        data = {
            "message": "Detection Completed successfully",
            "status": 200
        }
        return jsonify(data)
    except Exception as e:
        data = {
            "message": str(e),
            "status": 400
        }
        print(e)
        return jsonify(data)


@app.route('/api/detect_on_image', methods=['GET', 'POST'])
@cross_origin()
def process_image():
    if 'image' in request.files:
        category = request.args.get('category')
        image = request.files['image']
        input_file_path = 'static/uploads/' + image.filename
        root = os.path.abspath(os.path.dirname(__file__))
        segmented_path = Path(root, r'runs\segment')
        image.save(input_file_path)
        # Perform image processing here
        model = YOLO(fr"{category}.pt")
        results = model.predict(source=input_file_path, show=False, save=True)
        root = os.path.abspath(os.path.dirname(__file__))
        source = os.path.join(root, r'runs\segment\predict')
        destination = os.path.join(root, fr'static\uploads')

        if not os.path.exists(destination):
            os.makedirs(destination)
        # gather all files
        allfiles = os.listdir(source)

        # iterate on all files to move them to destination folder
        for f in allfiles:
            src_path = os.path.join(source, f)
            dst_path = os.path.join(destination, f)
            if os.path.exists(dst_path):
                os.remove(dst_path)
            os.rename(src_path, dst_path)
        if os.path.exists(segmented_path):
            shutil.rmtree(segmented_path)
        print(f"Results Saved at {destination}")
        # Return the URL or path of the processed image
        data = {
            "images": 'static/uploads/' + image.filename
        }
        return jsonify(data)
    return 'Image upload failed.'


@app.route('/')
@cross_origin()
def index():
    return render_template('single.html')


@app.route('/detect.html')
@cross_origin()
def detect_html_file():
    return render_template('detect.html')


if __name__ == '__main__':
    app.run(debug=False)
