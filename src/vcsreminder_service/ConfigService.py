import configparser
import os
import logging


from src.vcsreminder_object.profil import Profil

CONFFILE = 'profilConf.ini'

config = None

PROJECTPATH = 'projectpath'
REMINDERTIMEHOUR = 'remindertimehour'
REMINDERTIMEMIN = 'remindertimemin'
SELECTEDVCS = 'selectedvcs'
SLEEPTIME = 'sleeptime'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigService:
    
    

    def __init__(self):
        logger.info('Start: ini')
        self.config = configparser.ConfigParser()

    def reloadConfig(self):
        self.config = configparser.ConfigParser()

    def initConf(self):
        if os.path.isfile('./' + CONFFILE):
            logger.info('ConfigFile: {} exist.'.format(CONFFILE))
        else:
            logger.info('ConfigFile: {} dont exist.'.format(CONFFILE))
            self.createDefaultConf()

    def getSelections(self):
        self.config.read(CONFFILE)
        return self.config.sections()

    def getProfileBySelection(self, selection):
        self.config.read(CONFFILE)
        pp = ''
        rmh = 0
        rmm = 0
        svcs = ''
        st = 0
        for (each_key, each_val) in self.config.items(selection):
            if(each_key == PROJECTPATH):
                    pp = each_val
            if(each_key == REMINDERTIMEHOUR):
                    rmh = each_val
            if(each_key == REMINDERTIMEMIN):
                    rmm = each_val
            if(each_key == SELECTEDVCS):
                    svcs = each_val
            if(each_key == SLEEPTIME):
                    st = each_val
        return Profil(selection, rmh, rmm, pp, svcs, st)

    def readConf(self):
        self.config.read(CONFFILE)
        profilList = []
        for each_section in self.config.sections():
            
            pp = ''
            rmh = 0
            rmm = 0
            svcs = ''
            st = 0
            for (each_key, each_val) in self.config.items(each_section):
                if(each_key == PROJECTPATH):
                    pp = each_val
                if(each_key == REMINDERTIMEHOUR):
                    rmh = each_val
                if(each_key == REMINDERTIMEMIN):
                    rmm = each_val
                if(each_key == SELECTEDVCS):
                    svcs = each_val
                if(each_key == SLEEPTIME):
                    st = each_val
            profilList.append( Profil(each_section, rmh, rmm, pp, svcs, st))
        return profilList
        
    def createDefaultConf(self):
        logger.info('Start: createDefaultConf')
        self.config['DefaultProject'] = {PROJECTPATH: 'C:\\', REMINDERTIMEHOUR: 0, REMINDERTIMEMIN: 0, SELECTEDVCS : 'Git', SLEEPTIME: 5}
        self.config.write(open(CONFFILE, 'w'))

    def createNewProfile(self, profileName):
        
        self.config.read(CONFFILE)
        self.config[profileName] = {PROJECTPATH: 'C:\\', REMINDERTIMEHOUR: 0, REMINDERTIMEMIN: 0, SELECTEDVCS : 'Git', SLEEPTIME: 5}
        self.config.write(open(CONFFILE, 'w'))

    def deleteProfile(self, profileName):
        self.config.read(CONFFILE)
        self.config.remove_section(profileName)
        self.config.write(open(CONFFILE, 'w'))

    def saveProfile(self, profil):
        
        self.config.read(CONFFILE)
        self.config[profil.name] = {PROJECTPATH: profil.projectPath, REMINDERTIMEHOUR: profil.reminderTimeHour, REMINDERTIMEMIN: profil.reminderTimeMin, SELECTEDVCS : profil.choosenVCS, SLEEPTIME: profil.sleeptime}
        self.config.write(open(CONFFILE, 'w'))
        return self.readConf()