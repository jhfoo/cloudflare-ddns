# core
import argparse
import os
# import re
import logging
import time

# community
import uvicorn

# custom
import Client 
import util

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def initLogs():

  util.initLogger(logger)

def doServer(args):
  print (f"Listening on port {args.port}")

  isReload = args.dev
  uvicorn.run('Server:app', host = '0.0.0.0', port = args.port, log_level='debug', reload=isReload)

if __name__ == "__main__":
  initLogs()
  parser = argparse.ArgumentParser()
  subparser = parser.add_subparsers(dest='cmd', help = 'Client or server mode')

  ClientParser = subparser.add_parser('client')
  ClientParser.set_defaults(func = Client.doClient)
  ClientParser.add_argument('fqdn')
  ClientParser.add_argument('ApiToken', nargs='?')

  ServerParser = subparser.add_parser('server')
  ServerParser.add_argument('port', type=int, nargs='?', default = 5000)
  ServerParser.add_argument('-d','--dev', action = 'store_true')
  ServerParser.set_defaults(func = doServer)

  args = parser.parse_args()
  if args.cmd == None:
    print (parser.print_help())
  else:
    TimeStart = time.time()
    args.func(args)
    TimeTaken = int((time.time() - TimeStart)*1000)
    logger.info (f"{'Time taken'.ljust(Client.FIELD_LJUST)}: {TimeTaken}ms")