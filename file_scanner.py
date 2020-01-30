import os, io, argparse, re, fnmatch

# script path
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def match_rex(file, rex_items):
    # take the filename and validate if it matches the regex items
    for pat in rex_items:
        repat = fnmatch.translate(pat)
        match = re.search(repat, file)
        if match:
            return True

def find_files(dir_path, rex_items):
    for dir_path, sub_dir_list, file_list in os.walk(dir_path):
        for file in file_list:
            file_name = os.path.abspath(file)
            print(file_name)

def main():
    # arg parser
    parser = argparse.ArgumentParser()
    # make argument flags
    parser.add_argument('regexps', help='RE for file names', nargs='*')
    parser.add_argument('-i', '--src', help='Source folder to scan', required=True, type=str)
    parser.add_argument('-f', '--patfile', default='string', help='Patterns file')
    parser.add_argument('-o', '--dest', help='Output folder', required=True, type=str)
    args = parser.parse_args()
    print(args.src)
    #find_files(dir_path, rex_items)


if __name__ == "__main__":
    main()