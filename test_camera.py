from picamera2 import Picamera2
import time

#intialize
picam2 = Picamera2()
picam2.start()

print("Camera started. Capturing images for 5 seconds...")

#run camera 5 seconds until sleep
time.sleep(5)

picam2.stop()
print("Camera stopped.")
