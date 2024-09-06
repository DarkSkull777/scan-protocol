import requests
import argparse
import threading
from queue import Queue
import sys

putih = '\033[1;97m'
merah = '\033[1;91m'
hijau = '\033[1;92m'
kuning = '\033[1m\033[93m'
biru = '\033[1;94m'
reset = '\033[0m'

def check_protocol(domain):
    domain = domain.strip()
    if not domain:
        return None

    try:
        response = requests.get(f"https://{domain}", timeout=10, allow_redirects=False)
        if response.status_code < 400:
            return f"https://{domain}"
    except requests.exceptions.RequestException:
        pass

    try:
        response = requests.get(f"http://{domain}", timeout=10, allow_redirects=False)
        if response.status_code < 400:
            return f"http://{domain}"
    except requests.exceptions.RequestException:
        pass

    return None

def worker(queue, results, lock):
    while not queue.empty():
        domain = queue.get()
        protocol = check_protocol(domain)
        if protocol:
            with lock:
                print(f"{kuning}{domain}{reset} ~~>> {hijau}{protocol}{reset}")
                results.append(protocol)
        queue.task_done()

def main(args):
    queue = Queue()
    results = []
    lock = threading.Lock()

    if args.domain:
        print(f"{biru}Processing single target: {args.domain}{reset}")
        protocol = check_protocol(args.domain)
        if protocol:
            print(f"{kuning}{args.domain}{reset} ~~>> {hijau}{protocol}{reset}")
            results.append(protocol)
        else:
            print(f"{merah}Failed to determine protocol for {args.domain}{reset}")

    if args.list:
        try:
            with open(args.list, 'r') as f:
                domains = f.readlines()
                for domain in domains:
                    queue.put(domain.strip())

            for _ in range(args.threads):
                thread = threading.Thread(target=worker, args=(queue, results, lock))
                thread.start()

            queue.join()

        except FileNotFoundError:
            print(f"{merah}File {args.list} not found.{reset}")
            sys.exit(1)

    if args.output:
        try:
            with open(args.output, 'w') as f:
                for result in results:
                    f.write(result + '\n')
            print(f"{hijau}Process success... all results saved to {args.output}{reset}")
        except IOError as e:
            print(f"{merah}Error writing to {args.output}: {e}{reset}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect if domains use HTTP or HTTPS")
    parser.add_argument('-d', '--domain', help="Single target domain to check")
    parser.add_argument('-l', '--list', help="File containing list of domains to check")
    parser.add_argument('-o', '--output', help="File to save the results")
    parser.add_argument('-t', '--threads', type=int, default=30, help="Number of threads to use (default: 30)")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(0)

    main(args)
