import os
import cv2
import numpy as np
from Utils import PathManager
from Utils.ExpInfo import SingleLFIInfo


class RefocusingMask:
    def __init__(self,mask_file):
        self.mask_file=mask_file
        self.mask=cv2.imread(mask_file,cv2.IMREAD_GRAYSCALE)
        self.height,self.width=self.mask.shape

        self.mask_val_set=np.unique(self.mask)
        self.mask_val_set=[int(x) for x in self.mask_val_set if x>0]

    def GetMask(self):
        return self.mask
    
    def GetVal(self,h,w):
        return self.mask[h][w]
    
    def GetMaskSet(self):
        return self.mask_val_set
        
