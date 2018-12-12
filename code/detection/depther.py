import numpy as np
import hist_values
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

# def get_depth_of_color():
#     hist=hist_values.sample(n=5)
#     while(1):
#         depth=capture.get_depth()

    
    
    
    
