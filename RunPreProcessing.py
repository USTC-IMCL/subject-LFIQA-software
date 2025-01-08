import os
import sys
sys.path.append('./Utils')
import PreProcess
import DenseRefocusFunction
import numpy as np
import cv2
import json

lambda_file=None
meta_data=None
refocusing_folder=None
post_fix='.png'
angular_height=11
angular_width=11

def CalDenseRefocusing(img_path):
    test_img=os.path.join(img_path,'001_001.png')
    test_img=cv2.imread(test_img,-1)
    lf_image=np.zeros(angular_height,angular_width,)

