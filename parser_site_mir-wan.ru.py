from bs4 import BeautifulSoup
import requests
import os


def get_page(url, class_page):
    """ Функция отправляет по ссылке GET запрос для получения разметки html с тегом "а" и с указанным атрибутом class"""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    all_pages = soup.find_all('a', attrs={'class': class_page}, href=True)
    return all_pages


all_categories = get_page(url='https://mir-wan.ru', class_page='catline')
list_categories = []
list_category_url = []
list_items = []
list_item_url = []
os.mkdir('..\Catalogs')
for category in all_categories:
    list_categories.append(category.text)
    list_url = ('https://mir-wan.ru' + category.get('href'))
    list_category_url.append(list_url)
    if len(category.text) < 40:
        try:
            os.mkdir(f'..\Catalogs{category.text}')
        except FileExistsError:
            pass
        new_list_url = list_url.split('/')
        a = [id for id in new_list_url if id.isdigit()]
        if a:
            all_items = get_page(url=f"https://mir-wan.ru/tovar.php?t=sub&id={a[0]}", class_page='tovhead')
            for item in all_items:
                list_items.append(item.text)
                item_url = ('https://mir-wan.ru' + item.get('href'))
                list_item_url.append(item_url)
                req_for_item = requests.get(item_url)
                soup_for_item = BeautifulSoup(req_for_item.text, 'html.parser')
                all_item = soup_for_item.find_all('table')[12]
                description = all_item.find_all('tr')[0::]
                content = []
                for parameter in description:
                    parameter = str(parameter.text).replace('\xa0', '').replace('\n', '')
                    if parameter:
                        content.append(parameter)
                [content.remove(x) for x in content if content.count(x) > 1]
                name_file = content[0].replace('/', ' ')
                try:
                    with open(file=f'..\Catalogs\{category.text}\{name_file}.txt', mode='w', encoding='utf-8') as file:
                        file.write('\n'.join([y for y in content]))
                except FileNotFoundError:
                    pass

dict_cat_url = dict(zip(list_categories, list_category_url))
print(dict_cat_url, 'Количество категорий: ', len(dict_cat_url), sep='\n')
dict_item_url = dict(zip(list_items, list_item_url))
print(dict_item_url, 'Количество товаров: ', len(dict_item_url), sep='\n')
