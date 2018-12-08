import sys 
import logging

from PySide2 import QtWidgets
from src.vcsreminder_gui.setStyle import setPalette
from src.vcsreminder_service.SettingsUIService import SettingsUIService


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GuiService:

    def __init__(self):
        
        self.app = None
        self.settingUI = None
        
        self.iniGui()


    
    
    def iniGui(self):
        if self.app == None:
            logger.info('INI Application')
            self.app = QtWidgets.QApplication(sys.argv)
            logger.info('set Style')
            self.app.setStyle("Fusion")
            logger.info('set Palette')
            self.app.setPalette(setPalette())
        if self.settingUI == None:
            self.settingUI = SettingsUIService(self)

    def showAbout(self, name, content):
        print('showAbout')
        QtWidgets.QMessageBox.about(self.settingUI, name, content)