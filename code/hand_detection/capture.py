import cv2
import freenect
import frame_convert2

def get_video(cap,webcam=False):
    if webcam:
        if cap.isOpened():
            flag,frame=cap.read()
        else:
            flag=False
            frame=0
    else:
        frame=freenect.sync_get_video()[0]
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    return frame
    
def get_depth():
    depth=frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])
    return depth
