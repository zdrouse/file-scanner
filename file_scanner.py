import os, io, argparse, re, fnmatch, hashlib, sys, shutil

# script path
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def match_rex(file, rex_items):
    # take the filename and validate if it matches the regex items
    for pat in rex_items:
        repat = fnmatch.translate(pat)
        match = re.search(repat, file)
        if match:
            return True

def calculate_hash(file):
    try:
        with open(file, "rb") as f:
            f_bytes = f.read()
            f_hash = hashlib.sha256(f_bytes).hexdigest()
            return f_hash
    except Exception as e:
        print(f"Could not read file for hash: {e}... Exiting.")
        sys.exit(1)

def find_files(in_path, out_path, rex_items):
    print(rex_items)
    for in_path, sub_dir_list, file_list in os.walk(in_path):
        for file in file_list:
            file_name = os.path.abspath(file)
            #print(file_name)
            if match_rex(file_name, rex_items):
                file_hash = calculate_hash(file_name)
                print(f"{file_name} - {file_hash}")
                shutil.copy(file_name, out_path)

def main():
    # arg parser
    parser = argparse.ArgumentParser()
    # make argument flags
    parser.add_argument('regexps', help='RE for file names', nargs='*')
    parser.add_argument('-i', '--src', help='Source folder to scan', required=True, type=str)
    parser.add_argument('-f', '--patfile', default='string', help='Patterns file')
    parser.add_argument('-o', '--dest', help='Output folder', required=True, type=str)
    # parse the arguments
    args = parser.parse_args()
    # check if there are any regexps
    if args.patfile == 'string':
        if len(args.regexps) == 0:
            print("You must specify patterns in command line or as a file with -f option.")
            sys.exit(1)
        else:
            find_files(args.src, args.dest, args.regexps)
    else:
        try:
            with open(args.patfile, "r") as p:
                patterns = p.read().splitlines()
                find_files(args.src, args.dest, patterns)
        except Exception as e:
            print(f"Could not read file for patterns: {e}... Exiting.")
            sys.exit(1)

if __name__ == "__main__":
    main()