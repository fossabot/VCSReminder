# TODO Lizensen eintragen
import logging
import sys
import asyncio
import time
import random
import time

from datetime import datetime
from threading import Thread

from src.vcsreminder_service.SysTrayService import SysTrayService
from src.vcsreminder_service.ConfigService import ConfigService
from src.vcsreminder_service.VCSCheckService import VCSCheckService


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CHECK_ICO = 'src/vcsreminder_icons/bell_check.ico'
ERROR_ICO = 'src/vcsreminder_icons/bell_x.ico'
CHANGE_ICO = 'src/vcsreminder_icons/bell_clock.ico'

STATUS_OK = 'Git-Reminder Status: ok'
STATUS_CHANGE = 'Git-Reminder Status: Commit/Push erforderlich'
STATUS_ERROR = 'Git-Reminder Status: Repo nicht gefunden'

loopRun = False

class MainService:
        
    def __init__(self, *args, **kwargs):
        logger.info(' INI MainService')
        
        # 3 Erstelle Systray
        logger.info(' 3 INI Systray')
        self.sysTrayService = SysTrayService(self)
        self.sysTrayService.start()

        self.isRunning = False
        self.configService = ConfigService()
        self.threads = [] 


    def start(self):
        logger.info(' Start MainService')
        self.configService.reloadConfig()
        self.isRunning = True
        selections = self.configService.getSelections()
        logger.info(' {} Selections found'.format(len(selections)))
        
        logger.info(' {} Threads found'.format(len(self.threads)))
        for selection in selections:
            thread = Thread(target=self.profileThreads, args=(selection,))
            self.threads += [thread]
            thread.start()


    def stop(self):
        logger.info('Stop is called')
        self.isRunning = False
        logger.info(' {} Threads found to stop '.format(len(self.threads)))
        for x in  self.threads: 
            x.join()
        self.threads = []


    def restart(self):
        logger.info('Restart is called')
        self.stop()
        self.start()


    def profileThreads(self, selection):
        logger.info('Run profilThreads with: {} Selection'.format(selection))
        while self.isRunning:
            profile = self.configService.getProfileBySelection(selection)
            nowTime = datetime.now()
            targetTime = datetime(nowTime.year, nowTime.month, nowTime.day, int(profile.reminderTimeHour), int(profile.reminderTimeMin))
            if targetTime < nowTime:
                self.startCheckProfile(profile)
                logger.info('Set SleepTime: {} '.format(int(profile.sleeptime)))
                time.sleep(int(profile.sleeptime) * 60)
    
    

    def startCheckProfile(self, profile):
        logger.info('Run: startCheckProfile')
        vcsCheckService = VCSCheckService()
        profileStatus = vcsCheckService.checkVCS(profile)
        if(profileStatus == 0):
            self.sysTrayService.updateSystrayInfo(CHECK_ICO, STATUS_OK)
        if(profileStatus == 1):
            self.sysTrayService.updateSystrayInfo(CHANGE_ICO, STATUS_CHANGE)
        if(profileStatus == 2):
           self.sysTrayService.updateSystrayInfo(ERROR_ICO, STATUS_ERROR)