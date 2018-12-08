import logging

from PySide2 import QtWidgets, QtCore, QtGui

from src.vcsreminder_gui.settingsUI import Ui_Dialog
from src.vcsreminder_service.ConfigService import ConfigService
from src.vcsreminder_object.profil import Profil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SettingsUIService(QtWidgets.QDialog, Ui_Dialog):



    

    def __init__(self, mainservice, parent = None):
        super(SettingsUIService, self).__init__(parent)
        
        logger.info('Run: init')
        self.mainservice = mainservice
        self.setupUi(self)
        self.setWindowTitle('VCS-Reminder')
        self.setWindowIcon(QtGui.QIcon('src/vcsreminder_icons/bell_check.ico'))
        self.setFixedSize(400,300)

        
        logger.info('init configService')
        self.configService = ConfigService()
        
        # Fill Buttons
        logger.info('Fill Buttons')
        self.addProfileBtn.clicked.connect(self.addProfile)
        self.deleteProfileBtn.clicked.connect(self.deleteProfile)
        self.cancelBtn.clicked.connect(self.closeEvent)
        self.applyBtn.clicked.connect(self.saveAndCloseEvent)
        self.browseButton.clicked.connect(self.select_path)


        # Fill Dropdown
        logger.info('Fill Dropdown')
        sections = self.configService.getSelections()
        logger.info(' {} Sections found'.format(len(sections)))
        for s in sections:
            self.profileDropdown.addItem(s)
            logger.info(' Section Name : {}'.format(s))
        
        self.profile = None

        
        self.profile = self.configService.getProfileBySelection(self.profileDropdown.currentText())

        # Fill other Fields
        self.fillFields(self.profile)

        self.profileDropdown.currentIndexChanged.connect(self.dropdownindexChanged)

        # hide RadioButton Perforce
        self.radioButton_3.hide()
        
    

    def addProfile(self):
        logger.info('Run: addProfile')  
        text, ok = QtWidgets.QInputDialog.getText(self,'VCS_Reminder - Add Profile','Set Profile Name:')
        if ok:
            logger.info('Create Profile: {}'.format(text))
            self.configService.createNewProfile(text)
            self.reloadWidgetAfterAdd(text)
            self.mainservice.restart()
        else:
            logger.info('Run: addProfile''not ok')


    def deleteProfile(self):
        logger.info('Run: deleteProfile')

        dial = QtWidgets.QMessageBox()
        dial.setText('Delete Profile : ' + self.profileDropdown.currentText() + '?')
        dial.setWindowTitle("Caution!")
        dial.setIcon(QtWidgets.QMessageBox.Question)
        delete_YES = dial.addButton('Yes', QtWidgets.QMessageBox.YesRole) 
        dial.addButton('No', QtWidgets.QMessageBox.RejectRole)
        dial.exec_()
        if dial.clickedButton() == delete_YES:
            logger.info('Delete Profile : {}', self.profileDropdown.currentText())
            profile = self.configService.deleteProfile(self.profileDropdown.currentText())
            self.reloadWidgetAfterDelete(self.profileDropdown.currentIndex())
            self.mainservice.restart()

    def select_path(self):

        dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:',
                                       self.profile.projectPath,
                                       QtWidgets.QFileDialog.ShowDirsOnly)

        if dir:
            self.pathInput.setText(dir)
        else:
            pass

    def fillFields(self, profile):
        logger.info('Run: fillFields')
        self.profile = profile
        if self.profile.choosenVCS == 'Git':
            logger.info('git')
            self.radioButton.setChecked(True)
        elif self.profile.choosenVCS == 'SVN':
            logger.info('svn')
            self.radioButton_2.setChecked(True)
        elif self.profile.choosenVCS == 'Perforce':
            logger.info('perforce')
            self.radioButton_3.setChecked(True)
        else:
            logger.info('No VCS')

        self.repTime.setMinimum(0)
        self.repTime.setMaximum(1000)
        self.repTime.setProperty("value", self.profile.sleeptime)


        time = QtCore.QTime(int(self.profile.reminderTimeHour), int(self.profile.reminderTimeMin))
        self.reminderTime.setTime(time)


        self.pathInput.setText(self.profile.projectPath)

    def reloadWidgetAfterAdd(self, profilename):
        logger.info('Run: reloadWidgetAfterAdd')
        self.profileDropdown.insertItem(0, profilename)
        self.profileDropdown.setCurrentIndex(0)
        
        profile = self.configService.getProfileBySelection(self.profileDropdown.currentText())
        self.fillFields(profile)
    
    def reloadWidgetAfterDelete(self, currentindex):
        logger.info('Run: reloadWidgetAfterDelete')
        self.profileDropdown.removeItem(currentindex)
        self.profileDropdown.setCurrentIndex(0)
        
        profile = self.configService.getProfileBySelection(self.profileDropdown.currentText())
        self.fillFields(profile)
        
    def saveAndCloseEvent(self, event):
        self.apply()
        self.hide()


    def closeEvent(self, event):
        
        logger.info('Run: closeEvent')
        if self.isDirty():
            val = self.isChangedDialog()
            if val == 1:
                self.apply()
                self.hide()
            elif val == 2:
               self.hide()
            else:    
                pass
            
        else:
            self.hide()

    def dropdownindexChanged(self):
        logger.info('Run: dropdownindexChanged')
        
        profile = self.configService.getProfileBySelection(self.profileDropdown.currentText())
        if self.isDirty():
            val = self.isChangedDialog()
            if val == 1:
                self.apply()
                self.fillFields(profile)
            elif val == 2:
               self.fillFields(profile)
            else:
                pass
        else:
            self.fillFields(profile) 

    def isDirty(self):
        logger.info('Run: isDirty')
        isDirty = False

        if self.repTime.value() != int(self.profile.sleeptime):
            isDirty = True
        elif self.reminderTime.time().hour() != int(self.profile.reminderTimeHour):
            isDirty = True
        elif self.reminderTime.time().minute() != int(self.profile.reminderTimeMin):
            isDirty = True
        elif self.pathInput.text() != self.profile.projectPath:
            isDirty = True
        elif self.buttonGroup.checkedButton().text().lower() != self.profile.choosenVCS.lower():
            isDirty = True
        
        logger.info('IsDirty: {}'.format(isDirty))
        return isDirty

    def isChangedDialog(self):
        dial = QtWidgets.QMessageBox()
        dial.setText('The Profil: ' + self.profile.name + ' has been modified.')
        dial.setInformativeText("Do you want to save your changes?")
        dial.setWindowTitle("Caution!")
        dial.setIcon(QtWidgets.QMessageBox.Question)
        dial.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
        ret = dial.exec_()

        if ret == QtWidgets.QMessageBox.Save:
            return 1
        elif ret == QtWidgets.QMessageBox.Discard:
            return 2
        elif ret == QtWidgets.QMessageBox.Cancel:
            return 3
        else:
            return 3

    def apply(self):

        profile = Profil(self.profile.name, self.reminderTime.time().hour(), self.reminderTime.time().minute(), self.pathInput.text(), self.buttonGroup.checkedButton().text(), self.repTime.value())
        self.configService.saveProfile(profile)
        self.profile = profile
        self.mainservice.restart()
