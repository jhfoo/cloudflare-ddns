# cloudflare-ddns
Node client to updates DNS entry in Cloudflare

## Install
```
git clone https://github.com/jhfoo/cloudflare-ddns.git
```

## Usage
```
npm start <host.domain.name> <cloudflare api token>
```

## API Token Config
Create a token with the following permission:
- Zone -> DNS -> Edit

## What it does
1. Check if zone is managed by the token.
2. Get IP as reported by Cloudflare trace tool.
3. Create/ update host.domain.name with IP.

