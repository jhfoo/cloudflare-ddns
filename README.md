# cloudflare-ddns
## Purpose
The original goal was to create a simple Nodejs client that updates a Cloudflare DNS entry to the client's public IP,
much like DDNS. The new goal is to create a Python equivalent offering a server mode mimicking the same response as
Cloudflare's trace service. 

## Nodejs
Node client to updates DNS entry in Cloudflare

### Install
```
git clone https://github.com/jhfoo/cloudflare-ddns.git
```

### Usage
```
npm start <host.domain.name> <cloudflare api token>
```

### API Token Config
Create a token with the following permission:
- Zone -> DNS -> Edit

### What it does
1. Check if zone is managed by the token.
2. Get IP as reported by Cloudflare trace tool.
3. Create/ update host.domain.name with IP.

## Python (WIP)
### Install
```
git clone https://github.com/jhfoo/cloudflare-ddns.git
cd cloudflare-ddns/python
./bin/setup
```

### Usage
```
cd cloudflare-ddns/python
./bin/cloudflare-ddns client <hostname> <api token>
```

Alternatively the API token can be read from the environment variable CLOUDFLARE_TOKEN. If token
is passed in the CLI it supercedes the environment variable.