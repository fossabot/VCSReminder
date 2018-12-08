import logging
from src.vcsreminder_service.GuiService import GuiService
from src.vcsreminder_service.ConfigService import ConfigService
from src.vcsreminder_service.MainService import MainService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":

    # 1 ini MainService
    logger.info(' 1 INI MainService')
    mainService = MainService()
    
    # 2 Erstelle Config File wenn nicht vorhanden
    logger.info(' 2 INI Config File')
    configService = ConfigService()
    configService.initConf()

    # 3 Start VCS REMINDER
    logger.info(' 3 INI Start VCS Reminder')
    mainService.start()
  
    
   
