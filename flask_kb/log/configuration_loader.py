import logging
import os

import yaml


class ConfigurationLoader:
    
    def load_config(self, config_file_path):
        """
        The method will try to load the configuration
        to run the program.
        :param config_file_path: required configuration file path
        """
    
        # Set up logger
        logger = logging.getLogger(__name__)

        if os.path.exists(config_file_path):
            logger.debug("Application configuration file found: {0}"
                         .format(config_file_path))
            with open(config_file_path, 'rt') as f:
                config = yaml.safe_load(f.read())
                return config
        else:
            message = "Application configuration file NOT found, " \
                      "the application cannot start: {0}"\
                .format(config_file_path)
            logger.warning(message)
            raise OSError(message)
