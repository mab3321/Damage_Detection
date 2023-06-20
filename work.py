import cv2
import os
import shutil
import time
from pathlib import Path
from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import locale
locale.getpreferredencoding()
locale.getpreferredencoding = lambda: "UTF-8"


def predictor(source, weights, key, time_stamp_of_worker=''):
    try:
        root = os.path.abspath(os.path.dirname(__file__))
        segmented_path = Path(root, r'runs\segment')
        model = YOLO(fr"{weights}")
        results = model.predict(source=source, show=False, save=True)
        source = os.path.join(root, r'runs\segment\predict')
        destination = os.path.join(root, fr'results\{key}{str(time_stamp_of_worker)}')

        if not os.path.exists(destination):
            os.makedirs(destination)
        # gather all files
        allfiles = os.listdir(source)

        # iterate on all files to move them to destination folder
        for f in allfiles:
            src_path = os.path.join(source, f)
            dst_path = os.path.join(destination, f)
            os.rename(src_path, dst_path)
        if os.path.exists(segmented_path):
            shutil.rmtree(segmented_path)
        print(f"Results Saved at {destination}")
        return results
    except Exception as e:
        print(e)
        res = e


def Worker():

    paths = {}
    time_stamp_of_worker = time.time()
    target_path = os.path.abspath(os.path.dirname(__file__))
    path_for_body = os.path.join(target_path, "data", "body")
    paths["body"] = {
        "path": path_for_body,
        "weights": 'body.pt'
    }
    path_for_underbody = os.path.join(target_path, "data", "underbody")
    path_for_underbody_oilLeakage = os.path.join(path_for_underbody, "oilLeakage")
    path_for_underbody_rust = os.path.join(path_for_underbody, "rust")
    paths["underbody_oilLeakage"] = {
        "path": path_for_underbody_oilLeakage,
        "weights": 'oilLeakage.pt'
    }
    paths["underbody_rust"] = {
        "path": path_for_underbody_rust,
        "weights": 'rust.pt'
    }

    for key, val in paths.items():
        print(f"Starting Detection For {key}.Results Path Will be shown at the End.")
        predictor(time_stamp_of_worker=time_stamp_of_worker, source=val['path'], weights=val['weights'], key=key)


if __name__ == "__main__":
    Worker()
