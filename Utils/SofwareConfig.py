
from dataclasses import dataclass

@dataclass
class LFIWindowSize:
    width:int
    height:int
    font_size:int

software_config = {
    "Software_Version": "3.0.0",
    "Software_Path": "./",
    "Logs_Path": "./Logs",
    "Log_Level": "INFO"
    }

# session connector size
session_connector_size=LFIWindowSize(400,150,20)