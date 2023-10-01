import pip
from .Logger.python import Logger

DEPS = [
    'json5'
]

def install_package(pkg: str):
    pip.main(['install', pkg])

def install(logger: Logger):
    
    for dep in DEPS:
        try:
            __import__(dep)
            logger.success(f'Package {dep} is already installed.')
        except ImportError:
            logger.error(f'Failed to import {dep}')
            logger.info(f'Attempting to install now...')
            install_package(dep)
            logger.success(f'Successfully installed {dep}')
