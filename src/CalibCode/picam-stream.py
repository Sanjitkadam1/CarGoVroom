from picamera2 import Picamera2 # type: ignore
import time
import cv2 as cv
import numpy as np

cam = Picamera2()
config = cam.create_video_configuration(raw={"format": "SGBRG10", "size": (640, 480)})
cam.configure(config)

cam.start()
time.sleep(2)

try:
    while True:
        raw_frame = cam.capture_array("raw") #capture raw frame
        raw_frame = np.frombuffer(raw_frame, dtype=np.uint16).reshape(480,640) #convert to CV format
        raw_frame = (raw_frame / 1023.0 * 65535).astype(np.uint16) #normalize 10bit to 16bit
        rgb_frame = cv.cvtColor(raw_frame, cv.COLOR_BAYER_GB2BGR) #converts Bayer to RGB
        
        cv.imshow("Frame", rgb_frame)
        
        if cv.waitKey(1) & 0xff == ord('q'):
            break
        
finally:
    cam.stop()
    cv.destroyAllWindows()

