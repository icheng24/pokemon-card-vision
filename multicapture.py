from picamera2 import Picamera2
import time
from datetime import datetime
import cv2
import numpy as np
import json

NUM_FRAMES = 5      # capture 5 frames per camera and pick sharpest
WAIT_TIME = 1       # seconds between frames for auto-adjust
CROP_CENTER = True  # optional: crop center if card is centered

# function to measure sharpness (higher = sharper)
def measure_sharpness(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

# preprocess image for easier occipital character reconigiton or AI recognition
def preprocess_image(img):
    # grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # CLAHE (contrast enhancement)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    # adaptive threshold for text
    thresh = cv2.adaptiveThreshold(enhanced, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    # morphological operations to make text thicker (hopefully this does something)
    kernel = np.ones((2,2), np.uint8)
    morph = cv2.dilate(thresh, kernel, iterations=1)

    return morph

# loop over both cameras (front and back)
for cam_num in [0, 1]:  # 0 = front, 1 = back
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_file = f"photo_cam{cam_num}_raw_{timestamp}.jpg"
    proc_file = f"photo_cam{cam_num}_proc_{timestamp}.jpg"
    json_file = f"card_text_cam{cam_num}_{timestamp}.json"

    picam2 = Picamera2(camera_num=cam_num)
    config = picam2.create_still_configuration()
    picam2.configure(config)
    picam2.start()

    # capture multiple frames
    frames = []
    sharpness_vals = []
    for i in range(NUM_FRAMES):
        tmp_file = f"/tmp/frame_cam{cam_num}_{i}.jpg"
        picam2.capture_file(tmp_file)
        img = cv2.imread(tmp_file)
        if CROP_CENTER:
            h, w = img.shape[:2]
            crop_size = min(h, w)
            start_x = w//2 - crop_size//2
            start_y = h//2 - crop_size//2
            img = img[start_y:start_y+crop_size, start_x:start_x+crop_size]
        frames.append(img)
        sharpness_vals.append(measure_sharpness(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)))
        time.sleep(WAIT_TIME)

    picam2.stop()

    # pick the sharpest frame
    best_idx = np.argmax(sharpness_vals)
    best_frame = frames[best_idx]

    # save raw best frame
    cv2.imwrite(raw_file, best_frame)
    print(f"[{timestamp}] Camera {cam_num} RAW photo saved as {raw_file}")

    # preprocess for AI/OCR
    proc_img = preprocess_image(best_frame)
    cv2.imwrite(proc_file, proc_img)
    print(f"[{timestamp}] Camera {cam_num} PROCESSED photo saved as {proc_file}")

    # placeholder for modern AI OCR (replace with actual model later)
    extracted_text = "<AI OCR placeholder>"

    # save metadata
    data = {
        "camera": cam_num,
        "timestamp": timestamp,
        "raw_image": raw_file,
        "processed_image": proc_file,
        "sharpness": float(sharpness_vals[best_idx]),
        "ocr_text": extracted_text
    }
    with open(json_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[{timestamp}] Camera {cam_num} metadata saved as {json_file}\n")
