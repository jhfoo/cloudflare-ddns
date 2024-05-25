# core
import argparse
import os
import re
import time

# community
import uvicorn

# custom
from CloudflareClient import CloudflareClient

def doClient(args):
  FIELD_LJUST = 20
  TimeStart = time.time()

  try:
    ApiToken = None
    ApiSource = None

    if args.ApiToken:
      ApiSource = 'CLI'
      ApiToken = args.ApiToken
    elif 'CLOUDFLARE_TOKEN' in os.environ:
      ApiSource = 'environment'
      ApiToken = os.environ.get('CLOUDFLARE_TOKEN', None)
    else:
      raise Exception (f"Missing API token")

    client = CloudflareClient(ApiToken)
    print (f"{'Updating'.ljust(FIELD_LJUST)}: {args.fqdn}")
    PublicIp = client.getPublicIp()
    print (f"{'Detected public IP'.ljust(FIELD_LJUST)}: {PublicIp}")
    print (f"{'Token source'.ljust(FIELD_LJUST)}: {ApiSource}")

    zone = client.getZone(args.fqdn)
    ZoneId = zone['id']
    print (f"{'Zone Id'.ljust(FIELD_LJUST)}: {ZoneId}")

    DnsRecord = client.getDnsRecord(ZoneId, args.fqdn)
    if DnsRecord:
      RecordId = DnsRecord['id']
      print (f"{'Record Id'.ljust(FIELD_LJUST)}: {RecordId}")
      resp = client.updateDnsRecord(ZoneId, RecordId, args.fqdn, PublicIp)
      print (f"{'Update record'.ljust(FIELD_LJUST)}: {'OK' if resp['success'] else 'ERROR'}")
    else:
      resp = client.createDnsRecord(ZoneId, args.fqdn, PublicIp)
      print (f"{'Create record'.ljust(FIELD_LJUST)}: {'OK' if resp['success'] else 'ERROR'}")
      # print (f"[debug] {resp.text}")
    # doApiCall(f"{API_BASEURL}/zones/${args.fqdn}/dns_records")

  except Exception as err:
    print (f"\nERROR: {err}")

  TimeTaken = int((time.time() - TimeStart)*1000)
  print (f"{'Time taken'.ljust(FIELD_LJUST)}: {TimeTaken}ms")

def doServer(args):
  print (f"Listening on port {args.port}")

  isReload = args.dev
  uvicorn.run('Server:app', host = '0.0.0.0', port = args.port, log_level='debug', reload=isReload)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  subparser = parser.add_subparsers(dest='cmd', help = 'Client or server mode')

  ClientParser = subparser.add_parser('client')
  ClientParser.set_defaults(func = doClient)
  ClientParser.add_argument('fqdn')
  ClientParser.add_argument('ApiToken', nargs='?')

  ServerParser = subparser.add_parser('server')
  ServerParser.add_argument('port', nargs='?', default = 5000)
  ServerParser.add_argument('-d','--dev', action = 'store_true')
  ServerParser.set_defaults(func = doServer)

  args = parser.parse_args()
  if args.cmd == None:
    print (parser.print_help())
  else:
    args.func(args)