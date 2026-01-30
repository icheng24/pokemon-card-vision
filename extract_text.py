from picamera2 import Picamera2
import time
from datetime import datetime
import pytesseract
from PIL import Image
import json

# make a timestamp for both photo and json
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # e.g., 20260129_HrsMinsSecons
photo_file = f"photo_{timestamp}.jpg"
json_file = f"card_text_{timestamp}.json"

# set up the camera
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)

# start the camera and let it focus
picam2.start()
time.sleep(2)

# capture the image
picam2.capture_file(photo_file)
print(f"photo saved as {photo_file}")

# stop the camera
picam2.stop()

# open the image and extract text
img = Image.open(photo_file)
text = pytesseract.image_to_string(img)

# print extracted text
print("extracted text:")
print(text)

# save extracted text to JSON
f = open(json_file, "w")      # open the file for writing
json.dump({"textKey": text}, f)  # write the data to json library (.dump)
f.close()                      # close the file


print(f"[{timestamp}] text saved as {json_file}")
