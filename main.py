from main_workers import Send_Title
import os
import datetime
import requests
import json
from config import BASE_PATH, SHORT_NAME, AUTHOR_NAME, AUTHOR_URL


def get_postmen():
    '''
    Подгружает данные для telegraph из graph_bot.json,
    если файла не существует вызывает функцию регистрации
    '''
    try:
        with open('graph_bot.json') as f:
            graph_bot = json.load(f)
            data = {
                'access_token': graph_bot['access_token'],
                'author_name': graph_bot['author_name'],
                'author_url': graph_bot['author_url'],
                'return_content': False
            }
        return data
    except(Exception):
        return Create_Account()


def Create_Account():
    '''
    Функция регистрации использует данные из config.py(или cfg.env)
    для создания аккаунта в telegraph и сохраняет токен в graph_bot.json
    '''
    data = {
        'short_name': SHORT_NAME,
        'author_name': AUTHOR_NAME,
        'author_url': AUTHOR_URL
    }
    response = requests.get(
        "https://api.telegra.ph/createAccount?", params=data)
    answer = json.loads(response.content)
    if answer['ok']:
        with open('graph_bot.json', 'w', encoding='utf-8') as f:
            json.dump(answer['result'], f, ensure_ascii=False, indent=4)
        data = {
            'access_token': answer['access_token'],
            'author_name': answer['author_name'],
            'author_url': answer['author_url'],
            'return_content': False
        }
        return data
    else:
        raise Exception('Logging_Error')


def Get_Tiles():
    '''
    Возвращает список папок в рабочей папке
    '''
    try:
        lstOfTitles = os.listdir(BASE_PATH)
        try:
            lstOfTitles.remove('.DS_Store')
            return lstOfTitles
        except:
            return lstOfTitles
    except Exception as e:
        print("error in Get_Titles: ", str(e))
        return []


if __name__ == "__main__":
    Titles = Get_Tiles()
    postmen = get_postmen()
    counter = 1
    for Title in Titles:
        print(f'{counter}: {Title}')
        counter += 1
    answer = input('\nС каким тайтлом работаем? : ')
    if answer.isdigit() and int(answer) <= len(Titles):
        Title = Titles[int(answer) - 1]
        time_start = datetime.datetime.now()
        result = Send_Title(Title, postmen)
        print(f'{result}\n\n{datetime.datetime.now() - time_start}')
    else:
        print('Error input')
