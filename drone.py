# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import time

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen



def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0, # none
):
    # This function returns a string intended for the cmd line using the gstlaunch cmd
    # Each element in the described pipeline is seperated by an "!"
    # The "!" describes a simple link: the left is linked to the right.
    # In python stacking several strings consecutively creates a long string
    # 
    return (
        # NVIDIA camera GStreamer plugin that provides options to control 
        # ISP properties using the ARGUS API
        # Connects to the csi camera and provides a source for video
        "nvarguscamerasrc ! "
        # The following statements defines the capabilities of the pad.
        "video/x-raw(memory:NVMM), " # DMA buffer
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "

        # Converts videro from one colorspace to another & resizes (NV12 to GBRx)
        "nvvidconv flip-method=%d ! " # Element properties
        # Pad properties (source as it is the source for the next element in the pipeline)
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "

        # converts from BGRx to BGR and then connects it to the sink appsink
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )




def show_camera():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        # Creates Window
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        
        # While the window is still open
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret_val, img = cap.read()
            cv2.imshow("CSI Camera", img)
            
            keyCode = cv2.waitKey(1) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27:
                break
            
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")

def test_photo():
    #TODO Take a photo every second for 5 seconds

    # VideoCapture is a constructor that opens Camera I/O 
    # The first parameter is the file to be opened, in this case a gstreamer_pipeline
    # The second parameter is the API identifier, letting the VideoCapture constructor 
    # know how to open/ process the file
    #  
    # a gstreamer pipeline is used to instantiate the VideoCapture object

    print("Attempting to open Camera\n")
    cam = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    # Checking camera as opened
    if  not cam.isOpened():
        print("\n\n\nUnable to open Camera\n\n\n")
        return

    print("Camera Opened")
    
    start_time = time.time()
    time_passed = 0

    for i in range(1,6):

        time_passed = time.time() - start_time

        while time_passed < i:
             time_passed = time.time() - start_time
            
             pass

             print("Taking a photo\n")
             # take photo
             ret_val, img = cam.read()
            

             # save photo
             cv2.imwrite('test'+str(i)+'.png', img)


    # clean up
    cam.release()
    cv2.destroyAllWindows()





#If the file was run by itself, the function is run
if __name__ == "__main__":
    #show_camera()
    take_photo()