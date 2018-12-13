import freenect
import cv2
import numpy as np
import frame_convert2
 #config

depth_deviation=14
seed_increase=5
centre_extension=10
degree_thres = 80.0
 #####
def change_centre_extension(value):
     global centre_extension
     centre_extension=value
     
def change_depth_deviation(value):
     global depth_deviation
     depth_deviation=value

def change_seed_increase(value):
    global seed_increase
    seed_increase=value
    
def show_images(images, rows = 1, titles = None):
    """
    images=list of images
    """
    cols=len(images)/rows
    while(rows*cols<len(images)):
        cols+=1
    fig=plt.figure(figsize=(rows,cols))
    for i in range(len(images)):
        a=fig.add_subplot(rows,cols,i+1)
        a.set_title(titles[i])
        plt.imshow(images[i])

#function to get RGB image from kinect

 
#function to get depth image from kinect
def get_depth():
    depth=frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])
    return depth
    
    
def get_centre_mat(depth,k=centre_extension):
    h,w=depth.shape
    # c=depth[h//4:int(np.ceil(3*h/4)),w//4:int(np.ceil(3*w/4))]
    c=depth[h//2-k:h//2+k,w//2-k:w//2+k]
    return c
def get_median(array):
    array=array.reshape(-1)
    return np.median(array)
    
def get_mask(depth):
    global depth_deviation
    median=get_median(get_centre_mat(depth))
    mask=np.where(abs(depth-median)<=depth_deviation,128,0)
    # mask=np.where(abs(depth-median))
    mask=mask.astype(np.uint8)
    return mask
def morph_closing(mask):
    #dial,eros
    kernel=np.ones((3,3),np.uint8)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    return mask
def increase_seed(mask):
    global seed_increase
    k=seed_increase
    #assuming centre to be the seed point
    h,w=mask.shape
    # mask[((h//2)-k):np.ceil(h/2+k),((w//2)-k):np.ceil(w/2+k)]=128
    mask[h//2-k:h//2+k,w//2-k:w//2+k]=128
    return mask
def flood_fill(img):
    flood=img.copy()
    h,w=img.shape
    mask = np.zeros((h+2,w+2), np.uint8)
    cv2.floodFill(flood, mask, (h//2, w//2), 255, flags=4)
    return flood
    
def find_contours(image):
    _,contours,_=cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def clean_mask(depth):
    mask=get_mask(depth)
    mask=morph_closing(mask)
    mask=increase_seed(mask)
    mask=flood_fill(mask)
    return mask
    
def contour_defects(mask):
    mask_copy=mask.copy()
    contours=find_contours(mask_copy)
    max_contour=max(contours,key=cv2.contourArea)
    hull = cv2.convexHull(max_contour, returnPoints=False)
    defects = cv2.convexityDefects(max_contour, hull)
    return contours,defects
    
def angle_vec(v1, v2,rad=True):
    """
    angle between two vectors
    """
    #in degree
    angle=np.arctan2(np.linalg.norm(np.cross(v1, v2)),np.dot(v1, v2))
    if rad:
        angle=angle/180.0*np.pi
    return angle

def detect_fingers(contour,defects,img):
    global degree_thres
    thresh=degree_thres*np.pi/180
    # if(len(defects)<=2):
    #     return 0
    n=1
    #defect retru start,end,far,distan far and hull
    try:
        for i in range(defects.shape[0]):
            start_idx, end_idx,farthest_idx, _ = defects[i, 0]
            start = tuple(contour[start_idx][0])
            end = tuple(contour[end_idx][0])
            far = tuple(contour[farthest_idx][0])
            cv2.line(img, start, end, [0, 255,128], 2)
            diff=angle_vec(np.subtract(start,far),np.subtract(end,far))
            if (diff<thresh):
                n+=1
    except:
        pass
    n=min(5,n)
    
    return img
    

def runner():
    """
    images:[mask]
    """
    depth=get_depth()
    h,w=depth.shape
    mask=clean_mask(depth)
    contours,defects=contour_defects(mask)
    max_contour=max(contours,key=cv2.contourArea)
    mask_copy=cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
    mask_copy=detect_fingers(max_contour,defects,mask_copy)
    
    M = cv2.moments(max_contour)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    d_val=depth[cx,cy]
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(mask_copy,"centre:{}".format(d_val),(40,250), font, 2,(255,0,0),2,cv2.LINE_AA)
    
    cv2.drawContours(mask_copy,max_contour, -1, (0,255,0), 4)
    cv2.imshow('contoured',mask_copy)
    cv2.imshow('depth',depth)
    

cv2.namedWindow('contoured')    
cv2.namedWindow('depth')

win_name="depth"
cv2.createTrackbar('Deviation',win_name,depth_deviation,100,change_depth_deviation)
cv2.createTrackbar('Seed_increase',win_name,seed_increase,400,change_seed_increase)
cv2.createTrackbar('centre_extension',win_name,centre_extension,400,change_centre_extension)
print("starting")

while True:
    runner()
    if cv2.waitKey(10)==27:
        cv2.destroyAllWindows()
        break
print("stopped")

    
