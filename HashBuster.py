import hashlib, argparse, time, json, os
from random_word import RandomWords
from colorama import Fore

HASHES = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']

parser = argparse.ArgumentParser(description='Hash Buster')
subparsers = parser.add_subparsers(dest='command', help='Brute: Brute Force hashes with Rainbow Tables, Build: Generate Rainbow Tables from a wordlist')

parser_brute = subparsers.add_parser('brute', help='Brute force a hash with a Rainbow Table list')
parser_brute.add_argument('-H', '--hash', required=True, help='Targeted hash')
parser_brute.add_argument('-rt', '--rainbowtable', required=True, help='Rainbow Table list')
parser_brute.add_argument('-v', '--verbose', default=False, action='store_true', help='Verbose outputs, slows program')

parser_build = subparsers.add_parser('build', help='Generate Rainbow Tables from a wordlist.')
parser_build.add_argument('-o', '--output', required=True, help='Output file for Rainbow Table list')
parser_build.add_argument('-w', '--wordlist', required=True, help='Wordlist to generate Rainbow Table from')
parser_build.add_argument('-H', '--hash', required=True, choices=HASHES, help='Hash algorithm')
parser_build.add_argument('-v', '--verbose', default=False, action='store_true', help='Verbose outputs, slows program')

parser_checksum = subparsers.add_parser('checksum', help='Calculate checksum of a file.')
parser_checksum.add_argument('-f', '--file', required=True, help='File to calculate chechsum')
parser_checksum.add_argument('-H', '--hash', required=True, choices=HASHES, help='Hash algorithm')

parser_hashid = subparsers.add_parser('hashid', help = 'Identify a hash.')
parser_hashid.add_argument('-H', '--hash', required=True, help='Hash to identify')

parser_hash = subparsers.add_parser('hash', help='Hash a string.')
parser_hash.add_argument('-t', '--text', help='Text to hash.')
parser_hash.add_argument('-H', '--hash', required=True, choices=HASHES, help='Hash algorithm')
parser_hash.add_argument('-rw', '--random-word', default=False, action='store_true', help='Use a random word')

args = parser.parse_args()

def fileLen(file):
    length = 0
    with open(file, 'rb') as inputFile:
        for line in inputFile:
            length += 1
    return length

def hash(plaintext, alg):
    if alg == "md5": hash = hashlib.md5()
    elif alg == "sha1": hash = hashlib.sha1()
    elif alg == "sha224": hash = hashlib.sha224()
    elif alg == "sha256": hash = hashlib.sha256()
    elif alg == "sha384": hash = hashlib.sha384()
    elif alg == "sha512": hash = hashlib.sha512()

    hash.update(plaintext.encode())
    return hash.hexdigest()

def build():
    global COUNT

    print(f"[{Fore.YELLOW}*{Fore.RESET}] {Fore.MAGENTA}{fileLen(WORDLIST)}{Fore.RESET} total words, generating rainbow tables.")
    time.sleep(1)

    with open(OUTPUT, 'w') as output_file:
        with open(WORDLIST, 'rb') as wordlist_file:
            for line in wordlist_file:
                try:
                    word = line.strip().decode()
                    rt = word + ":" + hash(word, HASHALG)
                    output_file.write(rt + "\n")
                    if VERBOSE:
                        print(f"[{Fore.GREEN}#{COUNT}{Fore.RESET}] Added: {Fore.MAGENTA}{rt}{Fore.RESET}")
                        COUNT += 1
                except:
                    if VERBOSE: print(f"[{Fore.RED}#{COUNT}{Fore.RESET}] Failed to decode.")
                    pass
    
    print(f"\n[{Fore.GREEN}+{Fore.RESET}] Finished generating rainbow tables.")

def brute():
    print(f"[{Fore.YELLOW}*{Fore.RESET}] {Fore.MAGENTA}{fileLen(TABLES)}{Fore.RESET} total tables, starting Hash Buster.")
    time.sleep(1)

    with open(TABLES, 'rb') as rainbow_tables:
        for line in rainbow_tables:
            plaintext, hash = line.decode().strip().split(":")[0], line.decode().strip().split(":")[1]
            
            if hash == HASHALG:
                print(f"\n[{Fore.GREEN}+{Fore.RESET}] Found plaintext: {Fore.GREEN}{plaintext}{Fore.RESET}")
                exit()
            
            if VERBOSE:
                print(f"[{Fore.YELLOW}-{Fore.RESET}] Tried: {plaintext}:{hash}")

    print(f"\n[{Fore.RED}-{Fore.RESET}] Plaintext not found.")

def checksum():
    print(f"[{Fore.YELLOW}*{Fore.RESET}] {Fore.MAGENTA}{fileLen(FILE)}{Fore.RESET} total lines, calculating {HASHALG} checksum.")
    time.sleep(1)

    with open(FILE, 'rb') as file:
        data = file.read().decode()
        checksum = hash(data, HASHALG)
    
    print(f"\n[{Fore.GREEN}+{Fore.RESET}] {Fore.MAGENTA}{HASHALG}{Fore.RESET} checksum of {FILE}: {Fore.GREEN}{checksum}{Fore.RESET}")

def hashid():
    print(f"[{Fore.GREEN}+{Fore.RESET}] Hash ID of {Fore.YELLOW}{HASH}{Fore.RESET}:\n")
    print(os.system(f'hashid {HASH}'))


def hashText():
    hashed = hash(TEXT, HASHALG)
    print(f"[{Fore.GREEN}+{Fore.RESET}] {Fore.YELLOW}{TEXT}{Fore.RESET} hashed with {Fore.MAGENTA}{HASHALG}{Fore.RESET}: {Fore.GREEN}{hashed}{Fore.RESET}")

if __name__ == '__main__':
    if args.command == "brute":
        TABLES = args.rainbowtable
        HASHALG = args.hash
        VERBOSE = args.verbose

        brute()

    if args.command == "build":
        OUTPUT = args.output
        WORDLIST = args.wordlist
        HASHALG = args.hash
        VERBOSE = args.verbose
        COUNT = 0

        build()
    
    if args.command == "checksum":
        FILE = args.file
        HASHALG = args.hash

        checksum()
    
    if args.command == "hashid":
        HASH = args.hash

        hashid()
    
    if args.command == "hash":
        if args.text: TEXT = args.text
        if args.random_word: TEXT = RandomWords().get_random_word()
        HASHALG = args.hash

        hashText()
