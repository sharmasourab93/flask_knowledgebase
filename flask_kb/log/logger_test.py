from log.log_configurator import LogConfigurator
import time


LogConfigurator.setup_logging()
logger = LogConfigurator.get_logger(__name__)
logger.info("INFO Starting test")
logger.debug("DEBUG Starting test")
logger.warning("WARNING Starting test")
logger.critical("CRITICAL Starting test")
time.sleep(10)
logger.info("INFO Mid test")
logger.debug("DEBUG Mid test")
logger.warning("WARNING Mid test")
logger.critical("CRITICAL Mid test")
time.sleep(10)
logger.info("INFO End test")
logger.debug("DEBUG End test")
logger.warning("WARNING End test")
logger.critical("CRITICAL End test")
