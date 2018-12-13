import freenect
import cv2
import numpy as np

roi_list=[]
cx=100
cy=100
height=10
width=10
def find_roi():
    """
    returrn:
        rect=[(x1,y1),(x2,y2)]
    """
    centre=(cx,cy)

    def change_height(value):
        global height
        height=value
    def change_width(value):
        global width
        width=value
    def change_centre(value):
        global cx,cy
        cx-=value
        cy-=value

    def get_video():
        array,_ = freenect.sync_get_video()
        array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
        return array

    def draw_rectangle(img,centre,height,width):
        cx,cy=centre
        x1,y1=cx-width//2,cy+height//2
        x2,y2=x1+(width//2)*2,y1-(height//2)*2
        cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
        return [(x1,y1),(x2,y2)]

    def set_roi(img):
        global cx,cy,height,width
        cx=width
        cy=height
        centre=(cx,cy)
        rect=draw_rectangle(img,centre,height,width)
        cv2.imshow('calib',img)
        return rect

    cv2.namedWindow('calib')
    win_name='calib'    
    cv2.createTrackbar('Height',win_name,height,1000,change_height)
    cv2.createTrackbar('width',win_name,width,1000,change_width)    


    while(1):
        # print("start")
        frame=get_video()
        # print("frame")
        rect=set_roi(frame)
        if cv2.waitKey(10)==27:
            cv2.destroyAllWindows()
            break
    print("rect {}".format(rect))
    return rect
    
    
    
