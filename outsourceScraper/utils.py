import logging
import sys
import datetime as dt
import os


catalogs = {
    'vl':   {'Бухгалтерия': ['http://www.vl.ru/business/services-for-business/accountancy'],
             'Экономические': ['http://www.vl.ru/business/services-for-business/consulting-audit?search=аудит',
                        'http://www.vl.ru/business/services-for-business/consulting-audit?search=финансовый+консалтинг'
                ],
             'Логистика': ['http://www.vl.ru/taxi-transport-delivery/transportation/goods-traffic',
                           'http://www.vl.ru/taxi-transport-delivery/transportation/depot'],
             'IT': ['http://www.vl.ru/it-computers?search=аутсорсинг',
                    'http://www.vl.ru/it-computers?search=администрирование']
             },
    '2gis': {'Бухгалтерия': ['search/Бухгалтерские%20услуги'],
             'Экономические': ['search/Управленческий%20консалтинг', 'search/Аудиторские%20услуги'],
             'Логистика': ['search/Услуги%20складского%20хранения', 'search/Экспедирование%20грузов',
                           'search/Таможенное%20оформление'],
             'IT': ['search/Услуги%20системного%20администрирования', 'search/Автоматизация%20бизнес-процессов']}
}

cities = {
    'Хабаровск': 'khabarovsk',
    'Владивосток': 'vladivostok',
    'Уссурийск': 'ussuriysk',
    'Находка': 'nahodka',
    'Южно-Сахалинск': 'yuzhnosakhalinsk',
    'Комсомольск-на-Амуре': 'komsomolsk',
    'Благовещенск': 'blagoveshensk',
    'Якутск': 'yakutsk',
    'Петропавловск-Камчатский': 'p_kamchatskiy'
}

cities_to_region = {
    'Хабаровск': 27,
    'Владивосток': 25,
    'Уссурийск': 25,
    'Находка': 25,
    'Южно-Сахалинск': 65,
    'Комсомольск-на-Амуре': 27,
    'Благовещенск': 28,
    'Якутск': 14,
    'Петропавловск-Камчатский': 41
}


def setupLog(logToFile = False, path='.'):
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    ch.setFormatter(formatter)
    root.addHandler(ch)
    if logToFile:
        fileHandler = logging.FileHandler(os.path.join(path,
                                          r"log-{}.log".format(dt.datetime.now().strftime('%d-%m-%H-%M')))
                                        )
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(formatter)
        root.addHandler(fileHandler)
    logging.getLogger("requests").setLevel(logging.WARNING)