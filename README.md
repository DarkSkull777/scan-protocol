# scan-protocol
Scanning the protocol site from domain list. Detect if domains use HTTP or HTTPS

```
usage: scanprotocol.py [-h] [-d DOMAIN] [-l LIST] [-o OUTPUT] [-t THREADS]

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Single target domain to check
  -l LIST, --list LIST  File containing list of domains to check
  -o OUTPUT, --output OUTPUT
                        File to save the results
  -t THREADS, --threads THREADS
                        Number of threads to use (default: 30)```
