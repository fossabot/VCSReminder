import logging
import time

from win10toast import ToastNotifier
from git import Repo
from git import InvalidGitRepositoryError
from git import NoSuchPathError

import svn.local
from datetime import datetime


from src.vcsreminder_service.ConfigService import ConfigService

COMMITS_TO_PRINT = 1

COMMIT = 'commit'
DIRTY = 'dirty'
PUSH = 'push'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VCSCheckService:
       
    def showToastNotification(self, mainText, subText, iconPath):
        toaster = ToastNotifier()
        toaster.show_toast(mainText, subText,
                        icon_path=iconPath,
                        duration=5,
                        threaded=True)

    def checkVCS(self, profile):
        logger.info('Run: checkVCS')
        returnValue = 0
        vcs = profile.choosenVCS
        logger.info('Profile: {} has {} as VCS'.format(profile.name, vcs))
        if vcs == 'Git':
            currentProfileStatus = self.checkGitRepo(profile)
            returnValue = currentProfileStatus
        if vcs == 'SVN':
            self.checkSVNRepo(profile)
        if vcs == 'Perforce':
            self.checkPerforceRepo(profile)
        return returnValue

    def checkAllVCS(self):
        
        configService = ConfigService()
        logger.info('_________________________\n')
        logger.info('read current ConfSettings')
        profiles = configService.readConf()
        returnValue = 0
        logger.info('count Profils : ' + str(len(profiles)))
        for profile in profiles:
            logger.info('\nProfile Name : ' + profile.name)
            if profile.choosenVCS == 'git':
                currentProfileStatus = self.checkGitRepo(profile)
                if(currentProfileStatus>returnValue):
                    returnValue = currentProfileStatus
            if profile.choosenVCS == 'svn':
                self.checkSVNRepo(profile)

        return returnValue
 
    def isGitCommited(self, repo):
        commits_behind = repo.iter_commits('master..origin/master')
        commits_ahead = repo.iter_commits('origin/master..master')
        count = sum(1 for c in commits_ahead)
        if count == 0:
            return False
        else:
            return True

    def isGitDirty(self, repo):
            return repo.is_dirty()
    

    def checkGitRepo(self, profile):
        logger.info('Load Git Repository')
        returnValue =  0
        try:
            repo = Repo(profile.projectPath)
            if not repo.bare:
                logger.info('Repo at {} successfully loaded.'.format(profile.name))
                
                if  self.isGitDirty(repo):
                    returnValue = 1
                    self.showToastNotification('Please Commit and Push', 'Project {} has been changed'.format(profile.name), "src/vcsreminder_icons/bell_clock.ico")
                elif self.isGitCommited(repo):
                    returnValue = 1
                    self.showToastNotification('Please Push', 'Project {} has been changed'.format(profile.name), "src/vcsreminder_icons/bell_clock.ico")
                else:
                    returnValue = 0
            else:
                logger.info('Could not load repository at {} :('.format(profile.projectPath))
        except InvalidGitRepositoryError:
            logger.info('Repo at {} is not a Git Repo'.format(profile.projectPath))
            returnValue = 2
            self.showToastNotification('Error Invalid Git Repo', 'Repo at {} is not a Git Repo'.format(profile.name), "src/vcsreminder_icons/bell_x.ico")
        except NoSuchPathError:
            logger.info('Repo at {} is not found'.format(profile.projectPath))
            returnValue = 2
            self.showToastNotification('Error Repo not Found', 'Repo at {} is not exists in the filesystem'.format(profile.name), "src/vcsreminder_icons/bell_x.ico")
        return returnValue

    def checkSVNRepo(self, profile):
        logger.info('Load SVN Repository')
        returnValue =  0
        try:
            r = svn.local.LocalClient(profile.projectPath)
            status = {}
            for s in r.status():
                    if s.type == svn.constants.ST_MODIFIED:
                        returnValue = 1
                        self.showToastNotification('Please Commit', 'Project {} has been changed'.format(profile.name), "src/vcsreminder_icons/bell_clock.ico")
                        break
                    if s.type == svn.constants.ST_ADD:
                        returnValue = 1
                        self.showToastNotification('Please Commit', 'Project {} has been changed'.format(profile.name), "src/vcsreminder_icons/bell_clock.ico")
                        break
                    if s.type == svn.constants.ST_MISSING:
                        returnValue = 1
                        self.showToastNotification('Please Commit', 'Project {} has been changed'.format(profile.name), "src/vcsreminder_icons/bell_clock.ico")
                        break

        except svn.exception.SvnException:
            logger.info('Repo at {} is not found'.format(profile.projectPath))
            returnValue = 2
            self.showToastNotification('Error Repo not Found', 'Repo at {} is not exists in the filesystem'.format(profile.name), "src/vcsreminder_icons/bell_x.ico")
            
  
    def checkPerforceRepo(self, profile):
        # TODO Perforce anscheinend auch VCS (meint Kummerer!!!)
        pass



    def __init__(self):
        pass
