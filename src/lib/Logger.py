import logging
import os

import Variables


class Logger:

    def __init__(self):
        self.log_name = os.path.expanduser(os.path.join(Variables.ROOT, 'src.log'))
        self.level = logging.DEBUG
        self.logging = logging
        self.logging.basicConfig(
            filename=self.log_name,
            filemode='a',
            format='[%(asctime)s] %(name)s %(filename)-8s  %(levelname)s: %(message)s',
            datefmt='%H:%M:%S',
            level=self.level
        )

    def info(self, msg):
        self.logging.info(msg)

    def debug(self, msg):
        self.logging.debug(msg)

    def warning(self, msg):
        self.logging.warning(msg)

    def error(self, msg):
        self.logging.error(msg)
