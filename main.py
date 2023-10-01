import sys

from src.Converter import *
from src.reqs import install as installDependencies

from src.Logger.python import Logger

logger = Logger('BFAV2CP')
logger.time_format = '%H:%M:%S'

installDependencies(logger)

conversion = BFAV2CP(logger)

print(conversion)