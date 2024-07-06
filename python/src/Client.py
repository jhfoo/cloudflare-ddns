# core
import time
import logging

# custom
from CloudflareClient import CloudflareClient
import util

FIELD_LJUST = 20


def doClient(args):
  logger = logging.getLogger(__name__)
  util.initLogger(logger)

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
    logger.info (f"{'Updating'.ljust(FIELD_LJUST)}: {args.fqdn}")
    PublicIp = client.getPublicIp()
    logger.info (f"{'Detected public IP'.ljust(FIELD_LJUST)}: {PublicIp}")
    logger.info (f"{'Token source'.ljust(FIELD_LJUST)}: {ApiSource}")

    zone = client.getZone(args.fqdn)
    ZoneId = zone['id']
    logger.info (f"{'Zone Id'.ljust(FIELD_LJUST)}: {ZoneId}")

    DnsRecord = client.getDnsRecord(ZoneId, args.fqdn)
    if DnsRecord:
      RecordId = DnsRecord['id']
      logger.info (f"{'Record Id'.ljust(FIELD_LJUST)}: {RecordId}")
      resp = client.updateDnsRecord(ZoneId, RecordId, args.fqdn, PublicIp)
      logger.info (f"{'Update record'.ljust(FIELD_LJUST)}: {'OK' if resp['success'] else 'ERROR'}")
    else:
      resp = client.createDnsRecord(ZoneId, args.fqdn, PublicIp)
      logger.info (f"{'Create record'.ljust(FIELD_LJUST)}: {'OK' if resp['success'] else 'ERROR'}")
      # print (f"[debug] {resp.text}")
    # doApiCall(f"{API_BASEURL}/zones/${args.fqdn}/dns_records")

  except Exception as err:
    logger.error (f"\nERROR: {err}")

  