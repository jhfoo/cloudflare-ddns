# core
import json

# community
import requests

API_BASEURL = 'https://api.cloudflare.com/client/v4'

class CloudflareClient:
  def __init__(self, ApiToken):
    self.ApiToken = ApiToken

  def getPublicIp(self):
    resp = requests.get('https://www.cloudflare.com/cdn-cgi/trace')
    for line in resp.text.split('\n'):
      parts = line.split('=')
      if parts[0] == 'ip':
        return parts[1]

    return None

  def createDnsRecord(self, ZoneId, fqdn, IpAddr):
    resp = self.apiPost(f"/zones/{ZoneId}/dns_records", {
      'type': 'A',
      'name': fqdn,
      'content': IpAddr,
      'ttl': 60,
      'proxied': False,
    })
    return resp.json()

  def updateDnsRecord(self, ZoneId, RecordId, fqdn, IpAddr):
    resp = self.apiPut(f"/zones/{ZoneId}/dns_records/{RecordId}", {
      'type': 'A',
      'name': fqdn,
      'content': IpAddr,
      'ttl': 60,
      'proxied': False,
    })
    return resp.json()

  def getDnsRecord(self, ZoneId, fqdn):
    subpath = f'/zones/{ZoneId}/dns_records'
    RespJson = self.apiGet(subpath).json()

    if 'result' in RespJson:
      for rec in RespJson['result']:
        if rec['name'] == fqdn:
          return rec

      return None
    else:
      raise Exception(f'Unexpected response from {subpath}')

  def getZone(self, fqdn):
    RespJson = self.apiGet('/zones').json()
    if 'result' in RespJson:
      for zone in RespJson['result']:
        if zone['name'] in fqdn:
          return zone
    # else
    raise Exception('Unexpected response from /zones')

  def apiPost(self, url, data):
    resp = requests.post(API_BASEURL + url, json = data, headers = {
      'Authorization': f"Bearer {self.ApiToken}"
    })
    return resp

  def apiPut(self, url, data):
    # print (f"[debug] GET {API_BASEURL + url} {self.ApiToken}")
    resp = requests.put(API_BASEURL + url, json = data, headers = {
      'Authorization': f"Bearer {self.ApiToken}"
    })
    return resp

  def apiGet(self, url):
    # print (f"[debug] GET {API_BASEURL + url} {token}")
    resp = requests.get(API_BASEURL + url, headers = {
      'Authorization': f"Bearer {self.ApiToken}"
    })
    return resp
