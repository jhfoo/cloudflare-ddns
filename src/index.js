const CloudflareClient = require('./CloudflareClient')

validateArgs()

client = new CloudflareClient({
  ApiToken: process.argv[3],
})

const hostname = process.argv[2]
const domain = client.stripHost(hostname)

main(client)

async function main(client) {
  try {
    const zone = await client.getZoneInfo(domain)
    if (zone === null) {
      throw new Error(`No zone info found for ${domain}`)
    }

    const NewIp = await client.getTracedIp()
    const record = await client.getZoneRecord(zone.id, hostname)
    if (record === null) {
      // record does not exist: create
      const resp = await client.createRecord(zone.id, hostname, NewIp)
      console.log(resp)
    } else {
      //record exists: update
      const resp = await client.updateRecord(zone.id, hostname, NewIp, record.id)
      console.log(resp)
    }
  } catch (err) {
    console.error(err.message)
  }
}

function validateArgs() {
  if (process.argv.length < 3) {
    throw new Error('Missing argument: domain')
  }
  if (process.argv.length < 4) {
    throw new Error('Missing argument: API token')
  }
}