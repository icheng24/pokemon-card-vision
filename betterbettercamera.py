from picamera2 import Picamera2
import time
from datetime import datetime
import cv2
import numpy as np
import json
import os

# loop over both cameras:
for cam_num in [0, 1]:
    # timestamp to prevent overwriting files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_file_raw = f"photo_cam{cam_num}_raw_{timestamp}.jpg"
    photo_file_proc = f"photo_cam{cam_num}_proc_{timestamp}.jpg"
    json_file = f"card_text_cam{cam_num}_{timestamp}.json"

    # set up the camera
    picam2 = Picamera2(camera_num=cam_num)
    config = picam2.create_still_configuration()
    picam2.configure(config)

    # start camera
    picam2.start()
    
    # give camera 2 seconds to auto-adjust exposure/focus
    time.sleep(2)

    # capture raw photo
    picam2.capture_file(photo_file_raw)
    picam2.stop()
    print(f"[{timestamp}] Camera {cam_num} RAW photo saved as {photo_file_raw}")

    # process photo with OpenCV
    img = cv2.imread(photo_file_raw)

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # enhance contrast using CLAHE "Contrast Limited Adaptive Histogram Equalization" (contrast stretch)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) #split image into 8 grid
    enhanced = clahe.apply(gray)

    # sharpen image
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1], #focus on middle of each tile in grid
                       [0, -1, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)

    # save processed image
    cv2.imwrite(photo_file_proc, sharpened)
    print(f"[{timestamp}] Camera {cam_num} PROCESSED photo saved as {photo_file_proc}")

    # save JSON metadata
    data = {
        "camera": cam_num,
        "timestamp": timestamp,
        "raw_image": photo_file_raw,
        "processed_image": photo_file_proc,
        "note": "Processed image ready for OCR/LLM recognition"
    }
    with open(json_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[{timestamp}] Camera {cam_num} metadata saved as {json_file}\n")
