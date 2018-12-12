import numpy as np

def point_depth(depth,point,roi=3):
    """
    depth,point
    """
    k=roi
    roi=np.zeros((k,k))
    x,y=point
    
    median=depth[x-k:x+k,y-k:y+k]
    median=np.median(median)
    return median
    
    
    
    
