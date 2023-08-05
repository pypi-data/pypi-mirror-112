import argparse
import tempfile
from eventloop import on_file_changed
import os
import shutil
from colorama import Fore, Back, Style, init as colorama_init
import datetime
import string
import random
import glob

def random_suffix(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Logger():
    
    def print_info(self, msg):
        print(Fore.WHITE + now_str() + " " + Fore.YELLOW + Style.BRIGHT + msg + Fore.RESET + Style.NORMAL)

    def print_error(self, msg, with_date = True):
        if with_date:
            print(Fore.WHITE + now_str() + " ")
        print(Fore.RED + msg + Fore.RESET)

    def print_open(self, path):
        print(Fore.WHITE + now_str() + " open " + Fore.BLUE + Style.BRIGHT + path + Fore.RESET + Style.NORMAL)

def main():
    colorama_init()
    logger = Logger()

    parser = argparse.ArgumentParser(prog='watch-open')
    parser.add_argument('path', nargs='?')
    parser.add_argument('--include','-i', nargs='+', help="Include globs")
    parser.add_argument('--exclude','-e', nargs='+', help="Exclude globs")
    args = parser.parse_args()
    watch_path = args.path if args.path is not None else os.getcwd()

    #print(args); exit(0)

    include = args.include
    exclude = args.exclude
    if args.path is not None:
        watch_path = args.path
        if '*' in watch_path:
            include = [os.path.basename(watch_path)]
            watch_path = os.path.dirname(watch_path)
            if watch_path == '':
                watch_path = os.getcwd()
    else:
        watch_path = os.getcwd()

    if os.path.isdir(watch_path) and include is None:
        logger.print_error("Specify path and include")
        parser.print_help()
        exit(1)

    if os.path.isdir(watch_path):
        logger.print_info("Watching {} for {}".format(watch_path, " and ".join(include)))
    else:
        logger.print_info("Watching {}".format(watch_path))

    @on_file_changed(watch_path, include=include, exclude=exclude)
    def handler(file_path):

        dir_path = tempfile.mkdtemp(prefix='watch-open-')

        basename = os.path.basename(file_path)
        need_suffix = os.path.splitext(basename)[1].lower() in ['.xls','.xlsx','.xlsm']

        if need_suffix:
            basename = os.path.splitext(basename)[0] + "-" + random_suffix(4) + os.path.splitext(basename)[1]
        
        tmp_path = os.path.join(dir_path, basename)

        shutil.copy(file_path, tmp_path)
        os.startfile(tmp_path)
        logger.print_open(tmp_path)

if __name__ == "__main__":
    main()
