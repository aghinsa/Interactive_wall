import freenect
import numpy as np
import cv2
import config
import capture

side=config.side
number_of_rects=config.number_of_rects
which_contour=1


def draw_rectangles(frame,n=number_of_rects):
    global side,number_of_rects,rect1x,rect1y,rect2x,rect2y
    
    rows,cols,_=frame.shape
    rect1x = np.array(
        [6 * rows / 20, 6 * rows / 20, 6 * rows / 20, 
        9 * rows / 20, 9 * rows / 20, 9 * rows / 20, 
        12 * rows / 20,12 * rows / 20, 12 * rows / 20], dtype=np.uint32)
    rect1y = np.array([9 * cols / 20, 10 * cols / 20, 11 * cols / 20, 
        9 * cols / 20, 10 * cols / 20, 11 * cols / 20, 
        9 * cols / 20,10 * cols / 20, 11 * cols / 20], dtype=np.uint32)

    rect2x = rect1x + side
    rect2y = rect1y + side
    
    for i in range(n):
        cv2.rectangle(frame, (rect1y[i], rect1x[i]),
                      (rect2y[i], rect2x[i]),(0, 255, 0), 2)
    return frame
def get_hist(frame):
    global rect1x,rect1y,side,number_of_rects,side
    
    hsv_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    roi=np.zeros((number_of_rects*side,side,3),dtype=hsv_frame.dtype)
    for i in range(number_of_rects):
        roi[i*side:i*side+side,0:side]=hsv_frame[rect1x[i]:rect1x[i]+side,
                                        rect1y[i]:rect1y[i]+side]
                                        
    # hist=cv2.calcHist([roi],[0,1],None,[180, 256], [0, 180, 0, 256])
    hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    hist=cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
    return hist
    
def calib(frame):
    # frame=get_video(cap)
    frame=draw_rectangles(frame)
    hist=get_hist(frame)
    return hist
    
def calib_master(cap,n=4):
    hist_master=0
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    fontScale =5
    fontColor = (255,0,0)
    lineType = 2
    while(n>0):
        while(1):
            frame=capture.get_video(cap)
            h,w,_=frame.shape
            text_pos = (h//10,w//2)
            hist=calib(frame)
            cv2.putText(frame,str(n),text_pos, font, 
                fontScale,fontColor,lineType)
            cv2.imshow('frame',frame)
            if cv2.waitKey(10)==ord('s'):
                break
        hist_master+=hist    
        n-=1
    cv2.destroyAllWindows()
    return hist_master
