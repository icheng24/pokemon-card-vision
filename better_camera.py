from picamera2 import Picamera2
import time
from datetime import datetime
import cv2
import numpy as np
import json
import os

# iterate over both cameras (0 = front, 1 = back)
for cam_num in [0, 1]:
    # make timestamps so files don't overwrite each other
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_file_raw = f"photo_cam{cam_num}_raw_{timestamp}.jpg"
    photo_file_proc = f"photo_cam{cam_num}_proc_{timestamp}.jpg"
    json_file = f"card_text_cam{cam_num}_{timestamp}.json"

    # Capture photo
    picam2 = Picamera2(camera_num=cam_num)
    config = picam2.create_still_configuration()
    picam2.configure(config)

    picam2.start()
    time.sleep(2)  # give camera time to settle

    picam2.capture_file(photo_file_raw)
    picam2.stop()
    print(f"[{timestamp}] Camera {cam_num} RAW photo saved as {photo_file_raw}")

    # process image with OpenCV
    img = cv2.imread(photo_file_raw)

    # convert to grayscale for easier read
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # apply "Contrast Limited Adaptive Histogram Equalization"
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    # sharpen image
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)

    # reduce blur
    #sharpened = cv2.GaussianBlur(sharpened, (1,1), 0)

    # save processed image
    cv2.imwrite(photo_file_proc, sharpened)
    print(f"[{timestamp}] Camera {cam_num} PROCESSED photo saved as {photo_file_proc}")

    # json info save
    data = {
        "camera": cam_num,
        "timestamp": timestamp,
        "raw_image": photo_file_raw,
        "processed_image": photo_file_proc,
        "note": "Processed image ready for LLM/OCR recognition"
    }

    with open(json_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[{timestamp}] Camera {cam_num} metadata saved as {json_file}\n")
