import freenect
import cv2
import numpy as np
import roi

def get_depth():
    return freenect.sync_get_depth()[0]
    
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
    
def get_depth_of_roi(img,_roi):
    # depth=get_depth()
    rect=_roi
    #[(x1,y1),(x2,y2)]
    region=img[rect[0][0]:rect[1][0],rect[1][1]:rect[0][1]]
    median_depth=np.median(region.reshape(-1))
    return median_depth

def get_hist(img,_roi):
    img=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    region=img[_roi[0][0]:_roi[1][0],_roi[1][1]:_roi[0][1]]
    hist=cv2.calcHist([region], [0, 1], None, [180, 256], [0, 180, 0, 256])
    hist_norm=hist.copy()
    hist_norm=cv2.normalize(hist, hist_norm, 0, 255, cv2.NORM_MINMAX)
    return hist_norm
    
def hist_masking(img, hist):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    cv2.filter2D(dst, -1, disc, dst)
    ret, thresh = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)
    thresh = cv2.merge((thresh, thresh, thresh))
    return cv2.bitwise_and(frame, thresh)

# depth=get_depth()
# print(depth.shape)
frame=get_video()
_roi=roi.find_roi()
hist=get_hist(frame,_roi)
frame_mod=hist_masking(frame,hist)
cv2.imshow("ter",frame_mod)
# median_depth=get_depth_of_roi(depth,_roi)
# print("depth:{}".format(median_depth))
# 
# mask=np.where(depth==median_depth,1,0)

while(1):
    frame=get_video()
    
    
