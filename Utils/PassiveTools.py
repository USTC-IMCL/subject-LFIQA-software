import os
import cv2
import subprocess
from multiprocessing import Pool
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QPushButton,QApplication
import sys
import time

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
        cmd_pool.apply_async(subprocess.run, args=(cmd,), kwargs={'shell': True, 'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE})
    cmd_pool.close()
    cmd_pool.join()
    # get results from the pool
    results = [p.get() for p in cmd_pool._pool]
    return results

class CMDWorker(QThread):
    run_finished = Signal()
    num_progress = Signal(int,str)
    def __init__(self, cmds):
        super().__init__()
        self.cmds = cmds
        self.cmd_num= len(cmds)
        self.results=[]
        self.keep_runnning = True
        self.cmd_pool= Pool(4)
    
    def updateprogress(self,result):
        print(result)
        self.num_progress.emit(1,result)

    def run(self):
        for cmd in self.cmds:
            self.cmd_pool.apply_async(subprocess.run, args=(cmd,), callback= self.updateprogress )
        self.cmd_pool.close()
        self.cmd_pool.join()
        self.run_finished.emit()


class WorkerTest(QWidget):
    def __init__(self):
        super().__init__()
        self.btn = QPushButton('Run', self)
        self.worker=None
        self.btn.clicked.connect(self.RunCMD)
        self.already_done=0

    def UpdateDone(self,num,results):
        self.already_done+=num
        print(f"Already done {self.already_done}, results:{results}")

    def RunCMD(self):
        self.already_done=0
        self.worker=CMDWorker(['ffmpeg -version'])
        self.worker.run_finished.connect(self.RunFinished)
        self.worker.num_progress.connect(self.UpdateDone)
        self.worker.start()
    
    def RunFinished(self):
        self.worker.wait()
        self.worker.run_finished.disconnect(self.RunFinished)
        self.worker.num_progress.disconnect(self.UpdateDone)
        self.worker.deleteLater()
        self.worker=None
def square(n):
    return n * n

def print_result(result):
    print(f"Result: {result}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WorkerTest()
    window.show()
    sys.exit(app.exec())
    '''
    with Pool(processes=4) as pool:
        for  i in range(4):
            pool.apply_async(square,(i,),callback=lambda x: print_result(x))
        pool.close()
        pool.join()
    '''
