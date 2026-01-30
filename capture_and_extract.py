from picamera2 import Picamera2
import time
from datetime import datetime
import pytesseract
from PIL import Image
import json

# set up the cameras
for cam_num in [0, 1]:
    # create timestamp for each photo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_file = f"photo_cam{cam_num}_{timestamp}.jpg"
    json_file = f"card_text_cam{cam_num}_{timestamp}.json"
    
    # set up the camera
    picam2 = Picamera2(camera_num=cam_num)
    config = picam2.create_still_configuration()
    picam2.configure(config)

    # start camera and wait to focus
    picam2.start()
    time.sleep(2)

    # capture image
    picam2.capture_file(photo_file)
    picam2.stop()
    print(f"[{timestamp}] camera {cam_num} photo saved as {photo_file}")

    # read text from image
    img = Image.open(photo_file)
    text = pytesseract.image_to_string(img)

    # print extracted text
    print(f"Camera {cam_num} extracted text:")
    print(text)

    # save text to JSON
    f = open(json_file, "w") # open the file for writing
    json.dump({"textKey": text}, f) # write the data to json library (.dump)
    f.close() # close the file
    print(f"[{timestamp}] camera {cam_num} text saved as {json_file}")
