# core
import logging
import os
import pathlib

PATH_LOG = 'logs/'
FILE_LOG = 'cloudflare-ddns.log'

if not os.path.exists(PATH_LOG):
  os.makedirs(PATH_LOG)
  LogFile = pathlib.Path(PATH_LOG + FILE_LOG)
  LogFile.touch()


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(PATH_LOG + FILE_LOG)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(
  logging.Formatter('%(message)s')
)

def initLogger(logger):
  logger.setLevel(logging.DEBUG)
  logger.addHandler(file_handler)
  logger.addHandler(console_handler)
