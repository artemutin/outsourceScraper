from setuptools import setup, find_packages

setup(
    name='outsourceScraper'
    ,version='0.1.0'
    ,description='Парсим каталоги vl.ru и 2gis по ряду категорий'
    ,url=''
    ,author='Artem Utin'
    ,author_email='artemutin@yandex.ru'
    ,license='WTFPL'
    ,packages=find_packages(exclude=['contrib', 'docs', 'tests*'])
    ,install_requires=[
            'beautifulsoup4',
            'requests'
      ]
)