
from dataclasses import dataclass

@dataclass
class LFIWindowSize:
    width:int
    height:int
    font_size:int


# session connector size
session_connector_size=LFIWindowSize(400,150,20)