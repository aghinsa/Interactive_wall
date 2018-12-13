import numpy as np
import hist_values
def point_depth(depth,point,roi=5):
    """
    depth,point
    """
    k=roi
    roi=np.zeros((k,k))
    x,y=point
    
    median=depth[x-k:x+k,y-k:y+k]
    median=np.median(median)
    return median
    
def k2m(x,p1,p2):
    x1,y1=p1
    x2,y2=p2
    x=x-x1
    y=(y2-y1)/(x2-x1)
    y=y*x
    y=y+y1
    return y
    
    
def mask_with_distance(depth,distance,threshold,channel=1):
    # threshold=threshold/depth.max()
    mask=np.where(abs(depth-distance)<=threshold,1,0)
    # mask=(depth==distance)
    mask=mask.astype(np.uint8)
    return mask
    
    
    
    
    
