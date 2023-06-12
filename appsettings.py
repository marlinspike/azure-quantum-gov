import json
from typing import DefaultDict, List
from collections import defaultdict
import logging
from rich import print as rprint
from rich.text import Text
from rich.console import Console

CONFIG_FILE = 'env.json'
console = Console()
log_format = '%(asctime)s %(filename)s: %(message)s'
logging.basicConfig(filename='app.log', level=logging.DEBUG, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class AppSettings:

    def __init__(self, config_file:str, raw_json_input=False):
        '''
            Creates the AppSettings object
            Parameters:
                config_file (str): relative path to file
                raw_json_input (bool): True if config_file is a raw json string; False if it's a file 
        '''
        self.appsettings_file = CONFIG_FILE
        self.raw_json_input = raw_json_input
        self.settings = {}
        self.read_appsettings()
        
    
    def print_settings_json(self):
        console.print_json(json.dumps(self.settings, indent=3))


    def read_appsettings(self):
        try:
            logger.debug("Read settings")
            if(self.raw_json_input == True):
                self.settings = json.loads(self.appsettings_file)
            else:
                with open(self.appsettings_file) as data_file:
                    appsettings = json.load(data_file)
                    self.settings = appsettings
            return self.settings
        except Exception as e:
            logger.error("Unable to open config.json")
            console.print(f"There was an error reading appsettings from: {self.appsettings_file}")

    


if __name__ == '__main__':
    _app = AppSettings('env.json')
    settings_dict = _app.read_appsettings()
