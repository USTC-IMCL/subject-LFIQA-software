import os
import sys
sys.path.append('./Utils')
sys.path.append('./Widgets')
sys.path.append('./UI')
import PreProcess
import DenseRefocusFunction
import numpy as np
import cv2
import json



def CalDenseRefocusing(img_path):
    test_img=os.path.join(img_path,'003_003.png')
    test_img=cv2.imread(test_img,-1)
    img_height,img_width=test_img.shape[0],test_img.shape[1]
    lf_image=np.zeros((angular_height,angular_width,img_height,img_width,3),dtype=np.uint8)

    for row in row_range:
        for col in col_range:
            cur_view_path=os.path.join(img_path,f'{col:03d}_{row:03d}.png')
            temp=cv2.imread(cur_view_path,-1)
            if temp.max()>255:
                temp=temp//4#temp.max()*255
            lf_image[row-2,col-2]=temp.astype(np.uint8)
    
    with open(lambda_file,'r') as fid:
        meta_data=json.load(fid)
    min_lambda=meta_data['LambdaMin']
    max_lambda=meta_data['LambdaMax']

    device_meta=meta_data

    depth_map=cv2.imread(os.path.join(img_path,'depth.png'),cv2.IMREAD_GRAYSCALE)
    if depth_map.shape[0]!=img_height or depth_map.shape[1]!=img_width:
        depth_map=cv2.resize(depth_map,(img_width,img_height))

    all_depth_values=np.unique(depth_map)

    for depth_val in all_depth_values:
        output_name=os.path.join(refocusing_folder,f'{depth_val}.{post_fix}')
        if os.path.exists(output_name):
            continue
        refocus_img=DenseRefocusFunction.run_refocus(lf_image,device_meta,meta_data,depth_val,{'InterpMethod':'cubic'})
        output_img=refocus_img[:,:,:3]
        cv2.imwrite(output_name,output_img)

if __name__ == "__main__":
    view_root='/data_0/shengyang/Work/JPEG/LFIQA/examples/Bikes/Ori'
    lambda_file=os.path.join(view_root,'lambda.txt')
    meta_data=None
    angular_height=11
    angular_width=11
    refocusing_folder=os.path.join(view_root,'RefocusingViews')
    if not os.path.exists(refocusing_folder):
        os.mkdir(refocusing_folder)
    row_range=list(range(2,13))
    col_range=list(range(2,13))
    post_fix='.png'

    CalDenseRefocusing(view_root)

