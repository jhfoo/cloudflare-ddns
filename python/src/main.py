# core
import argparse

# community
import requests

def doClient(args):
  print ('I am the client')

def doServer(args):
  print ('I am the server')

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='cmd', help = 'Client or server mode')

ClientParser = subparser.add_parser('client')
ClientParser.set_defaults(func = doClient)
ServerParser = subparser.add_parser('server')
ServerParser.add_argument('host')
ServerParser.set_defaults(func = doServer)

args = parser.parse_args()
args.func(args)