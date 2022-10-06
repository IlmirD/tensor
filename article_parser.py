import sys
import os
import requests
import textwrap
from bs4 import BeautifulSoup

import parsing_parameter


class ParseArticle:
    url = ''
    name = ''
    path_to_file = ''
    tags = ['p'] # ищем текст в p теге
    string_width = 80 # максимальное количество столбцов или ширина строки

    # здесь формируем путь к файлу и название файла
    def __init__(self, url_address):
        self.url = url_address
        url_attr = self.url.split('/') # разбиваем url на массив и потом собираем из него путь и название файла
        if url_attr[-1] != '':
            self.name = url_attr[-1] + '.txt'
            self.path = os.getcwd() + '/'.join(url_attr[1:-1])
        else:
            # случай, если url оканчивается с .html. Просто вырезаем его
            self.name = url_attr[-2] + '.txt'
            self.path = os.getcwd() + '/'.join(url_attr[1:-2])
        if not os.path.exists(self.path):
            # создаем директорию
            os.makedirs(self.path)

    def save_file(self, text):
        file = open(str(self.path) + '/' + str(self.name), mode='w')
        file.write(text)
        file.close()

    def get_article(self):
        page = requests.get(self.url).text
        soup = BeautifulSoup(page, 'html.parser')
        # если указан тег для парсинга, ищем по нему
        tag = parsing_parameter.parsing_tag()
        if tag:
            result = soup.find_all(class_=tag)
        else:
            result = soup.find_all(self.tags)
        text = ''
        for r in result:
            if r.text != '':
                links = r.find_all('a')
                if links != '':
                    for link in links:
                        r.a.replace_with(link.text + str('[' + link['href'] + ']')) # помещаем ссылки в квадратные скобки
                text += ''.join(textwrap.fill(r.text, self.string_width)) + '\n\n'
        self.save_file(text)


if __name__ == '__main__' and (len(sys.argv) > 1):
        pa = ParseArticle(sys.argv[1])
        pa.get_article()