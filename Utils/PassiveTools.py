import os
import cv2
import subprocess
from multiprocessing import Pool
from PySide6.QtCore import QThread, Signal

def GetVideoInfo(video_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height

def ConcatPCFilesCMD(file_1,file_2,output_file,ffmpeg_path='ffmpeg'):
    ffmpeg_cmd=f"{ffmpeg_path} -i {file_1} -i {file_2} -filter_complex '[0:v]crop=w=iw/2:h=ih:x=iw/2:y=0[left];[1:v]crop=w=iw/2:h=ih:x=iw/2:y=0[right];[left][right]hstack=inputs=2' -c:v libx264 -qp 0 {output_file} -y"
    return ffmpeg_cmd

def RunCMDs(all_cmd):
    # print(cmd)
    cmd_pool=Pool(4)
    for cmd in all_cmd:
        cmd_pool.apply_async(subprocess.Popen, args=(cmd,), kwargs={'shell': True, 'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE})
    cmd_pool.close()
    cmd_pool.join()
    # get results from the pool
    results = [p.get() for p in cmd_pool._pool]
    return results

class CMDWorker(QThread):
    run_finished = Signal(list)
    num_progress = Signal(int)
    def __init__(self, cmds):
        super().__init__()
        self.cmds = cmds
        self.keep_runnning = True

    def run(self):
        RunCMDs(self.cmds)