import numpy as np
import cv2 
import freenect
import frame_convert2
import capture 
import calib
import contour_functions as cntfn
import config
import argparse

# parser=argparse.ArgumentParser()
# parser.add_argument("--input_dir","-i")
# args=parser.parse_args()
# data_dir=args.input_dir
n=1
parser=argparse.ArgumentParser()
parser.add_argument("--number_of_samples","-n",dest="num_samples",type=int)
args=parser.parse_args()
n=args.num_samples
cap=cv2.VideoCapture(0)
cv2.namedWindow("frame")
hist=calib.calib_master(cap,n)
np.save('hist_values',hist)
