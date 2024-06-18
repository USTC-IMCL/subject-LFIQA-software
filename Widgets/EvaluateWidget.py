from PySide6.QtWidgets import QStackedWidget, QWidget
from random import shuffle



class EvaluateWidget(QStackedWidget):
    def __init__(self,play_list=[]) -> None:
        super().__init__()
        self.play_list=play_list
        self.play_order=list(range(len(self.play_list)))
        self.cur_play_index=0
        self.finish_page=None
        '''
        TODO: how to describe the player list? 
        '''
        self.player_list=[]

    
    def ShuffleList(self):
        shuffle(self.play_order)
    



if __name__ == "__main__":
    pass

