import os
import cv2

input_path='/data_0/Work/JPEG/LFIQA/examples/Bikes/Ori/'

output_path='/data_0/Work/JPEG/LFIQA/examples/Bikes/dist/JPEG'

folder_1=os.path.join(output_path,'dist_1')
folder_2=os.path.join(output_path,'dist_2')
if not os.path.exists(folder_1):
    os.mkdir(folder_1)
if not os.path.exists(folder_2):
    os.mkdir(folder_2)

all_views=os.listdir(input_path)

quality_1=90

quality_2=10

for view_file in all_views:
    if '.txt' not in view_file and 'depth' not in view_file and '.png' in view_file:
        ori_img=cv2.imread(os.path.join(input_path, view_file))
        tmp_file_1=os.path.join(folder_1,'tmp.jpg')
        tmp_file_2=os.path.join(folder_2,'tmp.jpg')

        cv2.imwrite(tmp_file_1,ori_img,[int(cv2.IMWRITE_JPEG_QUALITY),quality_1])
        cv2.imwrite(tmp_file_2,ori_img,[int(cv2.IMWRITE_JPEG_QUALITY),quality_2])

        output_1=os.path.join(folder_1,view_file)
        tmp=cv2.imread(tmp_file_1)
        cv2.imwrite(output_1,tmp)

        output_2=os.path.join(folder_2,view_file)
        tmp=cv2.imread(tmp_file_2)
        cv2.imwrite(output_2,tmp)


os.remove(tmp_file_1)
os.remove(tmp_file_2)