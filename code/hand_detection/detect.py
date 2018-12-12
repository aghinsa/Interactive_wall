import numpy as np
import cv2 
import freenect
import frame_convert2
import capture 
import calib
import contour_functions as cntfn
import config
import depther

side=config.side
number_of_rects=config.number_of_rects
largest=config.largest
is_load=config.is_load
front_thresh=100

def change_front_thresh(value):
    global front_thresh
    front_thresh=value
    
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
      

def find_finger(frame):
    global largest
    k=largest
    contours=cntfn.find_contours(frame)
    sc= sorted(contours, key=lambda x: cv2.contourArea(x))
    try:
        max_contour=sc[-1]
        centre=cntfn.centroid(max_contour)
        cv2.circle(frame,centre, 5, [255, 0,0], -1)
    
        # if max_contour is not None:
        #     hull = cv2.convexHull(max_contour, returnPoints=False)
        #     defects = cv2.convexityDefects(max_contour, hull)
        #     far = cntfn.farthest_point(defects,max_contour, centre)
        #     cv2.circle(frame, far, 5, [0, 0, 255], -1)
            # cv2.line(frame,centre,far,[0,0,255],4)
    except:
        centre=(0,0)
        frame=np.zeros(frame.shape)
    return centre,frame

def frontal_mask(frame,depth):
    # global front_thresh
    gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    _,mask = cv2.threshold(gray,10,1, cv2.THRESH_BINARY)
    mask=mask.astype(np.float32)
    # 
    # mask=np.logical_and(depth,mask).astype(np.float32)
    # mask*=255
    # _,mask = cv2.threshold(mask,front_thresh,1, cv2.THRESH_BINARY)
    # mask=mask.astype(np.float32)
    # mask=(gray==0)
    # mask=np.logical_not(mask).astype(np.float32)
    depth=cv2.bitwise_and(depth,depth,mask)
    
    return depth
    return mask
                        
    
def main():    
    cap=cv2.VideoCapture(0)
    cv2.namedWindow("frame")
    # cv2.namedWindow("depth0")
    cv2.createTrackbar('Which Contour','frame',largest,10,change_largest)
    
    if not is_load:
        hist=calib.calib_master(cap)
    else:
        hist=np.load('hist_values.npy')
    cv2.namedWindow('depth')
    cv2.createTrackbar('Thresh','depth',front_thresh,250,change_front_thresh)
    point_sample_rate=30
    depth_list=np.zeros(point_sample_rate)
    
    while(1):
        frame=capture.get_video(cap)
        depth=capture.get_depth()
        depth=depth/depth.max()
        frame=hist_masking(frame,hist)
        centroid,frame=find_finger(frame)
        # depth=frontal_mask(frame,depth)
        
        
        if cv2.waitKey(10)==27:
            break
        median_depth=depther.point_depth(depth,centroid)
        i=0
        if i>=point_sample_rate:
            i=0
        depth_list[i]=median_depth
        md=np.mean(depth_list)*100
        cv2.imshow('depth',depth)
        capture.put_text(frame,str(md))
        cv2.imshow('frame',frame)
    cv2.destroyAllWindows()
    cap.release()

if __name__=="__main__":
    main()    
