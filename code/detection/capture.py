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
    
def get_depth(scale=True):
    depth=freenect.sync_get_depth()[0]
    if scale:
        depth=depth/depth.max()
            
    return depth

def put_text(frame,string,size=5,color=(255,0,0),text_pos=(0,0)):
    h,w,_=frame.shape
    text_pos = (h//10,w//2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale =size
    fontColor = color
    lineType = 2
    cv2.putText(frame,string,text_pos, font, 
        fontScale,fontColor,lineType)
    return frame
