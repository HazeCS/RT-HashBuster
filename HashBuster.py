import hashlib, argparse, time
from colorama import Fore

HASHES = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']

parser = argparse.ArgumentParser(description='Hash Buster')
subparsers = parser.add_subparsers(dest='command', help='Brute: Brute Force hashes with Rainbow Tables, Build: Generate Rainbow Tables from a wordlist')

parser_brute = subparsers.add_parser('brute', help='Brute force a hash with a Rainbow Table list')
parser_brute.add_argument('-H', '--hash', required=True, help='Targeted hash')
parser_brute.add_argument('-rt', '--rainbowtable', required=True, help='Rainbow Table list')
parser_brute.add_argument('-v', '--verbose', default=False, action='store_true', help='Verbose outputs, slows program')

parser_build = subparsers.add_parser('build', help='Generate rainbow tables from a wordlist.')
parser_build.add_argument('-o', '--output', required=True, help='Output file for rainbow table list')
parser_build.add_argument('-w', '--wordlist', required=True, help='Wordlist to generate rainbow table from')
parser_build.add_argument('-H', '--hash', required=True, choices=HASHES, help='Hash algorithm')
parser_build.add_argument('-v', '--verbose', default=False, action='store_true', help='Verbose outputs, slows program')

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

def build(output, wordlist, hashalg):
    global COUNT

    print(f"[{Fore.YELLOW}*{Fore.RESET}] {Fore.MAGENTA}{fileLen(WORDLIST)}{Fore.RESET} total words, generating rainbow tables.")
    time.sleep(1)

    with open(output, 'w') as output_file:
        with open(wordlist, 'rb') as wordlist_file:
            for line in wordlist_file:
                try:
                    word = line.strip().decode()
                    rt = word + ":" + hash(word, hashalg)
                    output_file.write(rt + "\n")
                    if VERBOSE:
                        print(f"[{Fore.GREEN}#{COUNT}{Fore.RESET}] Added: {Fore.MAGENTA}{rt}{Fore.RESET}")
                        COUNT += 1
                except:
                    if VERBOSE: print(f"[{Fore.RED}#{COUNT}{Fore.RESET}] Failed to decode.")
                    pass
    
    print(f"\n[{Fore.GREEN}+{Fore.RESET}] Finished generating rainbow tables.")

def brute():
    print(f"[{Fore.YELLOW}*{Fore.RESET}] {Fore.MAGENTA}{fileLen(TABLES)}{Fore.RESET} total tables, starting Hash Buster")
    time.sleep(1)

    with open(TABLES, 'rb') as rainbow_tables:
        for line in rainbow_tables:
            plaintext, hash = line.decode().strip().split(":")[0], line.decode().strip().split(":")[1]
            
            if hash == HASH:
                print(f"\n[{Fore.GREEN}+{Fore.RESET}] Found plaintext: {Fore.GREEN}{plaintext}{Fore.RESET}")
                exit()
            
            if VERBOSE:
                print(f"[{Fore.YELLOW}-{Fore.RESET}] Tried: {plaintext}:{hash}")

    print(f"\n[{Fore.RED}-{Fore.RESET}] Plaintext not found.")

if __name__ == '__main__':
    if args.command == "brute":
        TABLES = args.rainbowtable
        HASH = args.hash
        VERBOSE = args.verbose

        brute()

    if args.command == "build":
        OUTPUT = args.output
        WORDLIST = args.wordlist
        HASHALG = args.hash
        VERBOSE = args.verbose
        COUNT = 0

        build(OUTPUT, WORDLIST, HASHALG)
