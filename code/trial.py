from pykinect import nui
import numpy as np
import cv2

def video_handler(frame):
    video = numpy.empty((480,640,4),np.uint8)
    frame.image.copy_bits(video.ctypes.data)
    cv2.imshow('frame',video)

kinect=nui.Runtime()
kinect.video_frame_ready+=video_handler
kinect.video_frame_open(nui.ImageStreamType.Video,2,
                    nui.ImageResolution.Resolution640x480,
                    nui.ImageType.Color)
                    
    
cv2.namedWindow('frame')

while(1):
    if cv2.waitKey(1)==27:
        break
kinect.close()
cv2.destroyAllWindows()
