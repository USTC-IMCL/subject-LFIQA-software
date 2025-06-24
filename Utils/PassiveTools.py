import os
import cv2

def GetVideoInfo(video_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height

def ConcatPCFilesCMD(file_1,file_2,output_file,ffmpeg_path='ffmpeg'):
    ffmpeg_cmd=f"{ffmpeg_path} -i {file_1} -i {file_2} -filter_complex '[0:v]crop=w=iw/2:h=ih:x=iw/2:y=0[left];[1:v]crop=w=iw/2:h=ih:x=iw/2:y=0[right];[left][right]hstack=inputs=2' -c:v libx264 -qp 0 {output_file} -y"
    return ffmpeg_cmd