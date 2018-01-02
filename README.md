# Python-TeamCymru

A small Python wrapper for `whois.cymru.com`.

## Usage

```
from teamcymru import IPToASN

i2a = IPToASN([..list of ips..])
result = pc.lookup() # This returns a list of IPResult you can iterate through

for item in result:
    print(item.ip)
    print(item.asn)
    print(item.asn_cidr)
    print(item.asn_country_code)
    print(item.asn_registry)
    print(item.asn_date)
    print(item.asn_description)
    print(item.error)
```

## Install

No dependency required.

You can install python-teamcymru after cloning this repository with:

```
make setup
```

## Running tests

Install the dev-dependencies with `pip install -r dev-requirements.txt`

Run

```
make test
```
