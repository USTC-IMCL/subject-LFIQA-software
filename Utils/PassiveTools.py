import os
import cv2
import subprocess
from multiprocessing import Pool
from dataclasses import dataclass
from PySide6.QtCore import QThread, Signal, QThreadPool,QRunnable, QMutex, QMutexLocker, QObject
from PySide6.QtWidgets import QVBoxLayout,QProgressBar,QLabel
from PySide6.QtWidgets import QWidget, QPushButton,QApplication
import sys
import time
import json
import logging

def GetVideoInfo(video_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height

def ConcatPCFilesCMD(file_1,file_2,output_file,video_res=None,img_res=None,center_gap=20,ffmpeg_path='ffmpeg.exe'):
    if sys.platform == 'win32':
        ffmpeg_path = 'ffmpeg.exe'
    else:
        ffmpeg_path = 'ffmpeg'
    
    video_height, video_width = video_res
    img_height, img_width = img_res

    h_gap=(video_height-img_height)//2
    w_gap=(video_width-img_width*2-20)//2

    left_x=w_gap
    left_y=h_gap
    
    right_x=w_gap+img_width+center_gap
    right_y=h_gap

    ffmpeg_cmd=f"{ffmpeg_path} -i {file_1} -i {file_2} -i color=gray128 -filter_complex \"[0:v]crop=w={img_width}:h={img_height}:x={right_x}:y={right_y},pad=iw+20:ih:0:0:gray128[left];[1:v]crop=w={img_width}:h={img_height}:x={right_x}:y={right_y}[right];[left][right]hstack=inputs=2[ab];color=gray128:s={video_width}x{video_height}[bg];[bg][ab]overlay=x={left_x}:y={left_y}\" -c:v libx265 -qp 0 {output_file} -y"
    '''

    ffmpeg_cmd=f"{ffmpeg_path} -i {file_1} -i {file_2} -filter_complex \"[1:v]crop=w={img_width}:h={img_height}:x={right_x}:y={right_y}[right];[0:v][right]overlay=x={left_x}:y={left_y}\" -c:v libx265 -qp 0 {output_file} -y"
    '''
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

@dataclass
class CMDResult:
    idx:int
    cmd:str
    return_code:int
    stdout:str
    stderr:str

class CMDSignal(QObject):
    cmd_finished = Signal(CMDResult)
class CMDWorker(QRunnable):
    def __init__(self,idx,cmd):
        super().__init__()
        self.setAutoDelete(True)
        self.idx = idx
        self.cmd = cmd
        self.cmd_finished = CMDSignal()
    
    def run(self):
        try:
            cp = subprocess.run(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=7200)
            res=CMDResult(self.idx,self.cmd,cp.returncode,cp.stdout.decode('utf-8'),cp.stderr.decode('utf-8'))
        except subprocess.TimeoutExpired as e:
            res=CMDResult(self.idx,self.cmd,-1,'','Timeout')
        self.cmd_finished.cmd_finished.emit(res)

class WorkerManager(QObject):
    cmd_value_changed = Signal(int)
    def __init__(self,all_cmds=None,worker_num=4):
        super().__init__()
        self.worker_num=worker_num
        self.pool= QThreadPool()
        self.pool.setMaxThreadCount(worker_num)
        self.all_cmds = all_cmds
        self.logger = logging.getLogger("LogWindow")
        self.finished_work_num=0
        self._mutex = QMutex()
        self.error_cmds=[]
    
    def SetCMDs(self,cmds):
        self.all_cmds = cmds

    def RunTasks(self):
        for idx,cmd in enumerate(self.all_cmds):
            cur_worker=CMDWorker(idx,cmd)
            cur_worker.cmd_finished.cmd_finished.connect(self.OnWorkerFinished)
            self.pool.start(cur_worker)
        
    def OnWorkerFinished(self,cmd_result:CMDResult):
        with QMutexLocker(self._mutex):
            self.finished_work_num+=1
            self.logger.info(f"CMD {cmd_result.idx} finished, return code:{cmd_result.return_code}")
            if cmd_result.return_code!=0:
                self.error_cmds.append(cmd_result)
        self.cmd_value_changed.emit(self.finished_work_num)
    
    def Reset(self):
        self.finished_work_num=0
        self.cmd_value_changed.emit(self.finished_work_num)
        self.pool.clear()
        self.all_cmds=[]

'''
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
'''

class WorkerTest(QWidget):
    def __init__(self):
        super().__init__()
        self.btn = QPushButton('Run', self)
        self.worker=None
        self.btn.clicked.connect(self.RunCMD)
        self.already_done=0
        self.resize(400,150)
        

        vbox = QVBoxLayout(self)

        self.label=QLabel()
        self.label.setText("Click to start")
        vbox.addWidget(self.label)
        vbox.addWidget(self.btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.all_cmds=[]
        for i in range(100):
            self.all_cmds.append(f"sleep 0.{i%5+1}")
        vbox.addWidget(self.progress_bar)

        self.worker_manager=WorkerManager(self.all_cmds)
        self.worker_manager.cmd_value_changed.connect(self.UpdateProgress)

    def UpdateProgress(self,num):
        self.already_done=num
        self.label.setText(f"Running... Already done: {self.already_done}/{len(self.all_cmds)}")
        self.progress_bar.setValue(self.already_done)
        if self.already_done>=100:
            self.label.setText("Finished")
            self.btn.setEnabled(True)

    def RunCMD(self):
        self.already_done=0
        self.worker_manager.Reset()
        self.worker_manager.SetCMDs(self.all_cmds)
        self.worker_manager.RunTasks()
        self.progress_bar.setValue(0)
        self.label.setText("Running...")
        self.btn.setEnabled(False)
    
def square(n):
    return n * n

def print_result(result):
    print(f"Result: {result}")

if __name__ == '__main__':
    '''
    app = QApplication(sys.argv)
    window = WorkerTest()
    window.show()
    sys.exit(app.exec())
    with Pool(processes=4) as pool:
        for  i in range(4):
            pool.apply_async(square,(i,),callback=lambda x: print_result(x))
        pool.close()
        pool.join()
    '''

    video_1='./1.mp4'
    video_2='./2.mp4'

    video_res=[2160,4096]
    img_res=[540,1910]
    cmd=ConcatPCFilesCMD(video_1,video_2,'./output.mp4',video_res,img_res)
    print(cmd)
