# Python-TeamCymru

A small Python wrapper for `whois.cymru.com`.

## Usage

```python
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

## Pre-reqs (optional)

* Docker (latest)
* Docker Compose (latest)


## Testing the project

To build for the first time;

```
make build
```

To run a specific test:

```
make shell
pytest tests -k  you_special_test
```

To run the full test suite:

```
make test
```

To clean your environment:

```
make clean
```
