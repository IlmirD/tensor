import sys
import os
import textwrap
import re
from urllib.request import urlopen


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
        page = urlopen(self.url)
        html = page.read().decode('utf-8')

        pattern = r'<p(?:\s.*?)?>(.*?)</p>'
        result = re.findall(pattern, html)
        
        text = ''
        for r in result:
            link_text = re.findall(r'<a(?:\s.*?)?>(.*?)</a>', r)
            link = re.findall('href="([^"]*)', r)
            new_url = ' '.join(link_text) + ' ' + str(link)
            if link:
                new_string = re.sub(r'<a(?:\s.*?)?>(.*?)</a>', new_url, r)
                text += ''.join(textwrap.fill(new_string, self.string_width)) + '\n\n'
            else: 
                text += ''.join(textwrap.fill(''.join(r), self.string_width)) + '\n\n'
                
        self.save_file(text)
        
if __name__ == '__main__' and (len(sys.argv) > 1):
        pa = ParseArticle(sys.argv[1])
        pa.get_article()