import requests
from bs4 import BeautifulSoup
import config

URL = 'https://pogoda.mail.ru/country/russia'

#print(URL.removesuffix('country/russia'))
def get_html(url):
    response = requests.get(url)
    return response


def get_alphabet(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='cols__column__item cols__column__item_2')
    title_city = dict()
    for item in items:
        title_city[item.find('div', class_='city-list__title').get_text().strip('\n\t')] = \
            'http:' + item.find('div', class_='city-list__title').find('a').get('href')
    return title_city


def get_city(html, city):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='cols__column__item cols__column__item_3 cols__column__item_3_normal')
    city_list = dict()
    for item in items:
        city_list[item.find('div', class_="city-list__simple").get_text().strip('\n')] = \
            URL.removesuffix('/country/russia')+item.find('div', class_="city-list__simple").find('a').get('href')
    return city_list[city]


def get_temp_city(html):
    soup = BeautifulSoup(html, 'html.parser')
    #soup = soup.find('div', class_='information__content__wrapper information__content__wrapper_left')
    temp = soup.find('div', class_='information__content__temperature').get_text()#.find('span',class_='')
    #o = soup.find('div', class_='information__content__additional__item').get_text()
    png = soup.find('div', class_='information__content__additional information__content__additional_first')
    png = png.find('div', class_='information__content__additional__item').get_text()
    #print(png, temp)
    s = (temp.strip(), png.strip())
    return s


def parsing(url, city):
    html = get_html(url)
    if html.status_code == 200:
        alphabet = config.alphabet#get_alphabet(html.text)
        url = alphabet[city[0]]
        html = get_html(url)
        city_url = get_city(html.text, city)
        html = get_html(city_url)
        s = get_temp_city(html.text)
        print(type(s))
        return s
    else:
        s = 'Какието проблемы с сервером, попробуй позже'
        return s


def m():
    name_city = 'Москва'#input("write city").title()
    print(name_city)
    parsing(URL, name_city)
