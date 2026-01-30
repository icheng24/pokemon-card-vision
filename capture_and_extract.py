from picamera2 import Picamera2
import time
from datetime import datetime
import pytesseract
from PIL import Image
import json

# make a timestamp so our files don't overwrite each other
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
photo_file = f"photo_{timestamp}.jpg"
json_file = f"card_text_{timestamp}.json"

# set up the camera
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)

# start the camera and give it a second to focus
picam2.start()
time.sleep(2)

# take the picture and save it
picam2.capture_file(photo_file)
picam2.stop()
print(f"[{timestamp}] photo saved as {photo_file}")

# open the photo and read any text in it
img = Image.open(photo_file)
text = pytesseract.image_to_string(img) #must use pytesseract import

# show what we found
print("extracted text:")
print(text)

# save the text in a json file for later
f = open(json_file, "w")      # open the file for writing
json.dump({"textKey": text}, f)  # write the data to json library (.dump)
f.close()                      # close the file

print(f"[{timestamp}] text saved as {json_file}")
