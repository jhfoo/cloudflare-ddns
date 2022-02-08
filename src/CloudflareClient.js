const axios = require('axios')

const API_BASEURL = 'https://api.cloudflare.com/client/v4/',
  TRACE_URL = 'https://www.cloudflare.com/cdn-cgi/trace'

module.exports = class CloudflareClient {
  constructor(init) {
    this.ApiToken = init.ApiToken
  }

  async createRecord(ZoneId, hostname, ip) {
    const resp = await this.authPost(`zones/${ZoneId}/dns_records`, {
      type: 'A',
      name: hostname,
      content: ip,
      ttl: 60,
      proxied: false,
    })
    return resp.data
  }

  async updateRecord(ZoneId, hostname, ip, RecordId) {
    const resp = await this.authPut(`zones/${ZoneId}/dns_records/${RecordId}`, {
      type: 'A',
      name: hostname,
      content: ip,
      ttl: 60,
      proxied: false,
    })
    return resp.data
  }

  async getTracedIp() {
    const resp = await axios.get(TRACE_URL)
    const filtered = resp.data.split('\n').filter((line) => {
      return line.startsWith('ip=')
    })

    if (filtered.length > 0) {
      const matches = filtered[0].match(/^ip=(.+)$/)
      if (matches) {
        return matches[1]
      }
    }

    throw new Error('Unexpected server response calling trace url')
  }

  async getZoneRecord(ZoneId, hostname) {
    const records = await this.authGet(`zones/${ZoneId}/dns_records`)
    if ('result' in records.data) {
      const filtered = records.data.result.filter((item) => {
        return item.name === hostname
      })

      return filtered.length > 0 ? filtered[0] : null
    }

    throw new Error('Unexpected response retrieving dns records')
  }

  /// NOTE: does not handle more than 20 domains (needs to handle paging)
  async getZoneInfo(domain) {
    if (!domain) {
      throw new Error(`Invalidate domain param: ${domain}`)
    }
    const zones = await this.authGet(`zones`)

    if ('result' in zones.data) {
      const filtered = zones.data.result.filter((item) => {
        return item.name === domain
      })
      if (filtered.length > 0) {
        return filtered[0]
      } 
    }

    return null
  }

  stripHost(hostname) {
    console.log(`Matching: ${hostname}`)
    const matches = hostname.match(/^.+?\.(.*)$/)
    if (matches) {
      console.log(`Domain: ${matches[1]}`)
      return matches[1].toLowerCase()
    }

    return null
  }

  async authPut(PartialUrl, data) {
    return axios.put(`${API_BASEURL}${PartialUrl}`, data, {
      headers: {
        Authorization: `Bearer ${this.ApiToken}`,
      }
    })
  }

  async authPost(PartialUrl, data) {
    return axios.post(`${API_BASEURL}${PartialUrl}`, data, {
      headers: {
        Authorization: `Bearer ${this.ApiToken}`,
      }
    })
  }

  async authGet(PartialUrl) {
    console.log(`GET: ${API_BASEURL}${PartialUrl}`)
    return axios.get(`${API_BASEURL}${PartialUrl}`, {
      headers: {
        Authorization: `Bearer ${this.ApiToken}`,
      }
    })
  }
}

