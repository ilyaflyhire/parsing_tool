import requests             # библиотека для извлечения кода сайта
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pandas as pd

data = {}

for p in range(1, 100):

    url = f'https://www.citilink.ru/catalog/noutbuki/?view_type=list&p={p}'
    r = requests.get(url)
    sleep(randint(3,5))
    soup = BeautifulSoup(r.text, features='lxml')
    soup_string = str(r.text)

    product_card_code_mark = 'product_data__gtm-js'

    if product_card_code_mark in soup_string:

        print(f'------------------------------Выполняется парсинг товаров на странице {p}------------------------------')
        # перебираем все div с карточками товара
        products = soup.findAll('div', class_='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist')
        print('всего товаров на странице - ', len(products))

        for one_by_one in products:
            if one_by_one.find('div', class_='ProductCardHorizontal__not-available-block'):
                continue
            product_name_out = one_by_one.find('a', class_='ProductCardHorizontal__title Link js--Link Link_type_default').get('title').replace('  ', ' ')
            # print(product_name_out)
            product_price_out = one_by_one.find('span', class_='ProductCardHorizontal__price_current-price js--ProductCardHorizontal__price_current-price').text.replace(' ', '').replace('\n', '')
            # print(product_price_out)
            # data.append([product_name_out, int(product_price_out)])
            data.update({product_name_out: int(product_price_out)})
    else:
        break
print(data)

new_data = {}
print('-------------------------убираем слово Ноутбук из названия товара в словаре-------------------------')
for key in data:
        new_key = key.lstrip('Ноутбук ')
        new_data.update({new_key:data[key]})
print('-------------------------создаю dataframe в pandas-------------------------')
s_series = pd.Series(new_data)
print('-------------------------создаю excel file-------------------------')
s_series.to_excel('./Citilink_Laptops.xlsx')