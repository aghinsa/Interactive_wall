import numpy as np
import cv2 
import freenect
import frame_convert2
import capture 
import calib
import contour_functions as cntfn
import config
import depther
import argparse

side=config.side
number_of_rects=config.number_of_rects
is_load=config.is_load
front_thresh=100
which_contour=1

def change_front_thresh(value):
    global front_thresh
    front_thresh=value
    
def change_which_contour(value):
    global which_contour
    which_contour=value
    
def hist_masking(frame, hist):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    probab = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    cv2.filter2D(probab, -1, disc, probab)

    ret, thresh = cv2.threshold(probab, 150, 255, cv2.THRESH_BINARY)
    thresh = cv2.merge((thresh, thresh, thresh))

    return cv2.bitwise_and(frame, thresh)  
      

def find_centroid(frame):
    global which_contour
    contours=cntfn.find_contours(frame)
    sc= sorted(contours, key=lambda x: cv2.contourArea(x))
    try:
        max_contour=sc[-which_contour]
        centre=cntfn.centroid(max_contour)
        cv2.circle(frame,centre, 5, [0,255,255], -1)
        cv2.drawContours(frame,[max_contour],-1,(0,255,0),3)
    
        # if max_contour is not None:
        #     hull = cv2.convexHull(max_contour, returnPoints=False)
        #     defects = cv2.convexityDefects(max_contour, hull)
        #     far = cntfn.farthest_point(defects,max_contour, centre)
        #     cv2.circle(frame, far, 5, [0, 0, 255], -1)
            # cv2.line(frame,centre,far,[0,0,255],4)
    except:
        centre=(0,0)
        frame=np.zeros(frame.shape)+1
    return centre,frame

def main(save=False):    
    cap=cv2.VideoCapture(0)
    cv2.namedWindow("frame")
    # cv2.namedWindow("depth0")
    cv2.createTrackbar('Which Contour','frame',which_contour,10,change_which_contour)
    
    if not is_load:
        hist=calib.calib_master(cap)
    else:
        hist=np.load('hist_values.npy')
    # cv2.namedWindow('depth')

    point_sample_rate=10
    depth_list=np.zeros(point_sample_rate)
    i=0
    while(1):
        frame=capture.get_video(cap)
        depth=capture.get_depth()
        # depth=depth/depth.max()
        frame=hist_masking(frame,hist)
        centroid,frame=find_centroid(frame)

        if cv2.waitKey(10)==27:
            break
        median_depth=depther.point_depth(depth,centroid)
        
        i+=1
        if i>=point_sample_rate:
            i=0
        depth_list[i]=median_depth
        md=np.mean(depth_list)
        md=depther.k2m(md,(.4725,107),(.4372,66))
        # depth_scaled=depther.k2m(depth,(.4725,107),(.4372,66))
        # print(depth_scaled.min())
        
        print("{} {}".format(md,median_depth))
        # mask=depther.mask_with_distance(depth_scaled,71,threshold=2)
        # mask=np.expand_dims(mask,2)
        # frame=np.multiply(frame,mask)
        # print(np.sum(mask))
        # frame=mask
        
        if(abs(md-62)<2):
            capture.put_text(frame,'FML')
        # capture.put_text(frame,str(md),color=(0,0,255))
        depth_3=np.zeros(frame.shape)
        depth_3[:,:,0]=depth
        depth_3[:,:,1]=depth
        depth_3[:,:,2]=depth
        frame=frame/frame.max()+1e-16
        frame=np.hstack((frame,depth_3))
        cv2.imshow('frame',frame)
    if save:
        np.save('depth_list',depth_list)
    cv2.destroyAllWindows()
    cap.release()

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--save",'-s',type=bool,dest='save')
    args=parser.parse_args()
    save=args.save
    main(save)    
