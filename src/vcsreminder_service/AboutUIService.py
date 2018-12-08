import logging

from PySide2 import QtWidgets, QtCore, QtGui

from src.vcsreminder_gui.settingsUI import Ui_Dialog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AboutUIService(QtWidgets.QDialog, Ui_Dialog):


    

    def __init__(self, parent = None):
        super(AboutUIService, self).__init__(parent)
        
        logger.info('Run: init')
        self.setupUi(self)
        self.setWindowTitle('VCS-Reminder')
        self.setWindowIcon(QtGui.QIcon('src/vcsreminder_icons/bell_check.ico'))
        self.setFixedSize(400,300)

        
        
        
    