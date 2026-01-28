from picamera2 import Picamera2
import time
from datetime import datetime  # to get a timestamp for each photo

# set up the camera
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)

# start the camera and give it a sec to focus
picam2.start()
time.sleep(2)  # wait a bit so it can focus

# make a filename with a timestamp (so dont overwrite previous)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") #convert to a string
file_name = f"photo_{timestamp}.jpg"

picam2.capture_file(file_name)
print(f"photo saved as {file_name}")

picam2.stop()

