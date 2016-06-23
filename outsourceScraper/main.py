import sys
sys.path.append(".")

from outsourceScraper.Catalog import full_scrape
from outsourceScraper.utils import setupLog
from logging import exception, info
from sys import exc_info
from os.path import expanduser
import traceback
import datetime as dt
import argparse
import os


def main(path=expanduser('~'), max_threads=10, logTofile=True):
    try:
        if not path:
            path = expanduser('~')
        if not max_threads:
            max_threads = 10
        setupLog(logToFile=logTofile, path=path)
        info('Доступные параметры main: path=<Путь до желаемой папки для сохранения файла>')
        current_time = dt.datetime.now().strftime('%d-%m-%H-%M')


        full_scrape(os.path.join(path,'results-{}.csv'.format(current_time)), max_threads)
    except BaseException as e:
        exception('I caught an exception in main func! This should never ever been happen!:(. But Here it is: {}; callstask: {}'.
                  format(str(e), traceback.print_tb(exc_info()[2])))


if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Scrape some parts of vl.ru and 2gis catalogs')
        parser.add_argument('-p', dest='path', help='Specify folder to store files in.')
        parser.add_argument('-t', dest='max_threads', type=int, help="Specify number of threads to use.")
        parser.add_argument('-l', dest='logTofile', action='store_false', help="Set this flag to disable logging into file.")
        args = parser.parse_args()
        args = vars(args)
        if args.get('path', False):
            args['path'] = str(args['path'])
        main(**args)


