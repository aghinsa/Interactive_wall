import numpy as np
import cv2 

side=10
number_of_rects=9

def get_video(cap):
    
    if cap.isOpened():
        flag,frame=cap.read()
    else:
        flag=False
        frame=0
    return frame

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

def hist_masking(frame, hist):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    probab = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    cv2.filter2D(probab, -1, disc, probab)

    ret, thresh = cv2.threshold(probab, 150, 255, cv2.THRESH_BINARY)
    thresh = cv2.merge((thresh, thresh, thresh))

    return cv2.bitwise_and(frame, thresh)  
      
def centroid(max_contour):
    moment = cv2.moments(max_contour)
    if moment['m00'] != 0:
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
        return cx, cy
    else:
        return None
        
def find_contours(hist_mask_image):
    gray_hist_mask_image = cv2.cvtColor(hist_mask_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_hist_mask_image, 0, 255, 0)
    _, cont, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return cont
def farthest_point(defects, contour, centroid):
    if defects is not None and centroid is not None:
        s = defects[:, 0][:, 0]
        cx, cy = centroid

        x = np.array(contour[s][:, 0][:, 0], dtype=np.float)
        y = np.array(contour[s][:, 0][:, 1], dtype=np.float)

        xp = cv2.pow(cv2.subtract(x, cx), 2)
        yp = cv2.pow(cv2.subtract(y, cy), 2)
        dist = cv2.sqrt(cv2.add(xp, yp))

        dist_max_i = np.argmax(dist)

        if dist_max_i < len(s):
            farthest_defect = s[dist_max_i]
            farthest_point = tuple(contour[farthest_defect][0])
            return farthest_point
        else:
            return None

def find_finger(frame):
    contours=find_contours(frame)
    max_contour=max(contours,key=cv2.contourArea)
    centre=centroid(max_contour)
    cv2.circle(frame,centre, 5, [255, 0, 255], -1)
    
    if max_contour is not None:
        hull = cv2.convexHull(max_contour, returnPoints=False)
        defects = cv2.convexityDefects(max_contour, hull)
        far = farthest_point(defects,max_contour, centre)
        cv2.circle(frame, far, 5, [0, 0, 255], -1)
    return frame
    
        
def calib():
    frame=get_video(cap)
    frame=draw_rectangles(frame)
    hist=get_hist(frame)
    return hist
def main():    
    cap=cv2.VideoCapture(0)
    cv2.namedWindow("frame")
    while(1):
        frame=get_video(cap)
        frame=draw_rectangles(frame)
        hist=get_hist(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(10)==27:
            break
    while(1):
        frame=get_video(cap)    
        frame=hist_masking(frame,hist)
        frame=find_finger(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(10)==27:
            break
        
    
    cv2.destroyAllWindows()
    cap.release()

if __name__=="__main__":
    main()    
