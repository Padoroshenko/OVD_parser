import argparse
import requests
import pandas
from bs4 import BeautifulSoup

def main(args):

    url = args.url
    filename = args.filename
    result =[] # Результирующий список для вывода в файл. Формат [['Name','tel1','tel2' ... ],[],...]
    response = requests.get(url)
    soup = BeautifulSoup(response.text,features="lxml")
    maxTelsCount=0 # максимальное количество телефонов для одного ОВД. Используется для определения количества колонок
    for ultag in soup.findAll('ul', {'class': 'goverment_list_simple'}): # Ищем списки ОВД по округам
        for litag in ultag.findAll('li'): # Обрабатываем каждое ОВД в округе
            ovdName = (litag.text)  # Получаем название ОВД
            ovdInfo = [] # Информация по ОВД. Формат ['Name','tel1','tel2' ... ]
            ovdInfo.append(ovdName.replace(u'\xa0', u' '))
            ovdUrl = litag.find('a',href=True)['href']
            response = requests.get(ovdUrl) # открываем ссылку для поиска телефонов ОВД
            ovdPage=BeautifulSoup(response.text,features="lxml")
            contact = ovdPage.find('div', {'class': 'contact'})
            tels = contact.find('dt',string="Телефон:").find_next_siblings('dd') # Получаем список телефонов по ОВД
            if(len(tels)>maxTelsCount):
                maxTelsCount=len(tels)
            for tel in tels: # Выделяем телеоны отдельно. Вносим в ovdInfo
                ovdInfo.append(tel.text.replace(u'\xa0', u' ').split('—')[0].replace(' ',''))
            if(filename is not None): # Если необходимо вывести в файл, добавляем в результирующий список. Иначе выводим в консоль
                result.append(ovdInfo)
            else:
                print(ovdInfo)
    if filename is not None: # Запись в файл
        cols = ['Name']
        for i in range(maxTelsCount):
            cols.append('Tel'+str(i+1))
        df = pandas.DataFrame(result,columns=cols)
        df.to_excel(filename)


parser = argparse.ArgumentParser(description='Process some integers.') #Создаем парсер
parser.add_argument('-u', action='store',dest='url', help='URL',required=True)
parser.add_argument('-f',action='store',dest='filename', help='Name if output file')
args = parser.parse_args()
main(args)