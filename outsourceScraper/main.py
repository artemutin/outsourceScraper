from outsourceScraper.Catalog import full_scrape
from outsourceScraper.utils import setupLog
from logging import exception, info
from sys import exc_info
from os.path import expanduser
import traceback
import datetime as dt


def main(path=expanduser('~')):
    try:
        setupLog(logToFile=True, path=path)
        info('Доступные параметры main: path=<Путь до желаемой папки для сохранения файла>')
        current_time = dt.datetime.now().time().isoformat()
        full_scrape(path+'/results-{}.csv'.format(current_time))
    except BaseException as e:
        exception('I caught an exception in main func! This should never ever be happend!:(. But Here it is: {}; callstask: {}'.
                  format(str(e), traceback.print_tb(exc_info()[2]) ))


if __name__ == "__main__":
    main()


