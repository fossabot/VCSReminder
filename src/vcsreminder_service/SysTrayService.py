
import logging
import sys

from infi.systray import SysTrayIcon

from PySide2 import QtWidgets

from src.vcsreminder_gui.setStyle import setPalette
from src.vcsreminder_service.AboutUIService import AboutUIService
from src.vcsreminder_service.SettingsUIService import SettingsUIService


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHECK_ICO = 'src/vcsreminder_icons/bell_check.ico'
ERROR_ICO = 'src/vcsreminder_icons/bell_x.ico'
CHANGE_ICO = 'src/vcsreminder_icons/bell_clock.ico'

STATUS_OK = 'Git-Reminder Status: ok'
STATUS_CHANGE = 'Git-Reminder Status: Commit/Push erforderlich'
STATUS_ERROR = 'Git-Reminder Status: Repo nicht gefunden'


class SysTrayService:

    def __init__(self, mainService):
        logger.info('Run : ini')
        self.app = None
        self.aboutUI = None
        self.settingUI = None
        
        self.mainService = mainService

    def start(self):
        # TODO notification anpassen (kein ToolTip)
        logger.info('Run: iniSystray')
        menu_options = (("Settings", None, self.openSettings),("Restart", None, self.restart),("About", None, self.about),)
        self.systray = SysTrayIcon(CHECK_ICO, STATUS_OK, menu_options,  on_quit=self.on_quit_callback)
        logger.info('systray start')
        self.systray.start()
    
    
    def about(self, systray):

        # TODO About Anpassen
        self.iniAboutUI()
        aboutText = '<html><head/><body><p>Utility to get a notification to commit and/or push the repository</p><p><br/>Developed by Christian Beigelbeck \
        </p><p>\
        Licensed under the <a href="https://www.gnu.org/licenses/gpl-3.0-standalone.html"><span style=" text-decoration:\
         underline; color:#2980b9;">GPL v3 license</span></a></p><p>Project home: \
         <a href="https://overmindstudios.github.io/BlenderUpdater/"><span style=" text-decoration:\
         underline; color:#2980b9;">https://www.github.io/VCSReminder/</a></p> \
         Application version: ' + '0.0.1' + '</body></html> '
        
        QtWidgets.QMessageBox.about(self.aboutUI, 'About', aboutText)

    def on_quit_callback(self, systray):
        logger.info('Run: on_quit_callback')
        self.mainService.stop()

    def updateSystrayInfo(self, ico, status):
        self.systray.update(ico, status)

    def restart(self, systray):
        logger.info('Run: restart')
        self.mainService.restart()
    

    def openSettings(self, systray):
        
        logger.info('Run: openSettings')
        self.iniSettingUI()
        logger.info('exec settingUI')
        self.settingUI.exec()
        self.app.exec_()

      
        
    def iniAboutUI(self):
            if self.app == None:
                logger.info('INI Application')
                self.app = QtWidgets.QApplication(sys.argv)
                logger.info('set Style')
                self.app.setStyle("Fusion")
                logger.info('set Palette')
                self.app.setPalette(setPalette())
            if self.aboutUI == None:
                self.aboutUI = AboutUIService()
    
    
    def iniSettingUI(self):
        if self.app == None:
            logger.info('INI Application')
            self.app = QtWidgets.QApplication(sys.argv)
            logger.info('set Style')
            self.app.setStyle("Fusion")
            logger.info('set Palette')
            self.app.setPalette(setPalette())
        if self.settingUI == None:
            self.settingUI = SettingsUIService(self.mainService)

    