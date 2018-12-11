import numpy as np
import cv2 
import freenect
import frame_convert2
import capture 
import calib
import contour_functions as cntfn
import config

side=config.side
number_of_rects=config.number_of_rects
largest=config.largest

def change_largest(value):
    global largest
    largest=value
    
def hist_masking(frame, hist):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    probab = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    cv2.filter2D(probab, -1, disc, probab)

    ret, thresh = cv2.threshold(probab, 150, 255, cv2.THRESH_BINARY)
    thresh = cv2.merge((thresh, thresh, thresh))

    return cv2.bitwise_and(frame, thresh)  
      

def find_finger(frame,):
    global largest
    k=largest
    contours=cntfn.find_contours(frame)
    sc= sorted(contours, key=lambda x: cv2.contourArea(x))
    max_contour=sc[-k]
    centre=cntfn.centroid(max_contour)
    cv2.circle(frame,centre, 5, [255, 0, 255], -1)
    
    if max_contour is not None:
        hull = cv2.convexHull(max_contour, returnPoints=False)
        defects = cv2.convexityDefects(max_contour, hull)
        far = cntfn.farthest_point(defects,max_contour, centre)
        cv2.circle(frame, far, 5, [0, 0, 255], -1)
        cv2.line(frame,centre,far,[0,0,255],4)
    return frame

def mask_infront(frame,depth,thres=0):
    mask=np.where(frame<=thres,0,1)
    masked_depth=cv2.bitwise_and(depth,depth,mask=mask)
    return masked_depth
                        
    
def main():    
    cap=cv2.VideoCapture(0)
    cv2.namedWindow("frame")
    cv2.namedWindow('depth')
    cv2.createTrackbar('Change Contour','frame',largest,10,change_largest)
    
    hist=calib.calib_master(cap)
    
    while(1):
        frame=capture.get_video(cap)
        depth=capture.get_depth()    
        frame=hist_masking(frame,hist)
        frame=find_finger(frame)
        cv2.imshow('frame',frame)
        cv2.imshow('depth',depth)
        if cv2.waitKey(10)==27:
            break
        
    
    cv2.destroyAllWindows()
    cap.release()

if __name__=="__main__":
    main()    
