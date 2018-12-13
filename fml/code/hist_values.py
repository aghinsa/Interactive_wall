import numpy as np
import cv2 
import freenect
import frame_convert2
import capture 
import calib
import contour_functions as cntfn
import config
import argparse

def sample(n,save=False):
    cap=cv2.VideoCapture(0)
    cv2.namedWindow("frame")
    hist=calib.calib_master(cap,n)
    if save:
        np.save('hist_values',hist)
    return hist

    
if __name__=="__main__":
    n=1
    parser=argparse.ArgumentParser()
    parser.add_argument("--number_of_samples","-n",dest="num_samples",type=int)
    args=parser.parse_args()
    n=args.num_samples
    sample(n,save=True)
    
