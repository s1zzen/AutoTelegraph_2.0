import requests
import json
from config import BASE_PATH, SHORT_NAME, AUTHOR_NAME, AUTHOR_URL, ttStartMenu1
from osdirectcontroller import Get_Tiles, Get_Files_Names


class Telegraph_Postmen():
    def __init__(self):
        try:
            with open('graph_bot.json') as f:
                graph_bot = json.load(f)
            self.access_token = graph_bot['access_token']
            self.author_name = graph_bot['author_name']
            self.author_url = graph_bot['author_url']
        except (Exception):
            self.Create_Account()

    def Create_Account(self):
        # создаем параметры для создания профиля
        data = {
            'short_name': SHORT_NAME,
            'author_name': AUTHOR_NAME,
            'author_url': AUTHOR_URL
        }
        # отправляем запрос ответ понадобится, запишем в переменную:
        response = requests.get(
            "https://api.telegra.ph/createAccount?", params=data)
        answer = json.loads(response.content)
        if answer['ok']:
            with open('graph_bot.json', 'w', encoding='utf-8') as f:
                # сохраняю в файл graph_bot
                json.dump(answer, f, ensure_ascii=False, indent=4)
            print(answer)
            self.access_token = answer['result']['access_token']
            self.author_name = answer['result']['author_name']
            self.author_url = answer['result']['author_url']
            return answer
        else:
            raise Exception('Error')

    def Image_Upload(self, title, file):
        '''
        Sends a file to telegra.ph storage and returns its url
        Works ONLY with 'gif', 'jpeg', 'jpg', 'png', 'mp4'

        Parameters
        ---------------
        path_to_file -> str, path to a local file

        Return
        ---------------
        telegraph_url -> str, url of the file uploaded

        >>>telegraph_file_upload('test_image.jpg')
        https://telegra.ph/file/16016bafcf4eca0ce3e2b.jpg
        >>>telegraph_file_upload('untitled.txt')
        error, txt-file can not be processed
        '''
        path_to_file = f'{BASE_PATH}{title}\\{file}'
        file_types = {'gif': 'image/gif', 'jpeg': 'image/jpeg',
                      'jpg': 'image/jpg', 'png': 'image/png',
                      'mp4': 'video/mp4'}
        file_ext = path_to_file.split('.')[-1]

        if file_ext in file_types:
            file_type = file_types[file_ext]
        else:
            return f'error, {file_ext}-file can not be proccessed'

        with open(path_to_file, 'rb') as f:
            url = 'https://telegra.ph/upload'
            response = requests.post(
                url, files={'file': ('file', f, file_type)})

        telegraph_url = json.loads(response.content)
        if 'error' in telegraph_url:
            print(f'\n\n\n\n{telegraph_url["error"]}\n\n\n\n')
            return None
        telegraph_url = telegraph_url[0]['src']
        telegraph_url = f'https://telegra.ph{telegraph_url}'
        print(telegraph_url)
        return telegraph_url

    def Send_Post(self, title, content):
        data = {
            'access_token': self.access_token,
            'title': title,
            'author_name': self.author_name,
            'author_url': self.author_url,
            'content': content,
            'return_content': False
        }
        create_page = requests.post(
            'https://api.telegra.ph/createPage?', json=data)
        return json.loads(create_page.content)

    def Send_Title(self, title):
        Files_Names = Get_Files_Names(title)
        print(Files_Names)
        Files_urls = []
        for file in Files_Names:
            src = self.Image_Upload(title=title, file=file)
            if not src:
                continue
            Files_urls.append({'tag': 'img', 'attrs': {'src': src}})
        exit = self.Send_Post(title=title, content=Files_urls)
        print(exit)
        if exit['ok']:
            url = exit['result']['url']
            print(f'url ---> {url}')
        else:
            print('GG')


if __name__ == "__main__":
    print(ttStartMenu1)
    Titles = Get_Tiles()
    counter = 1
    for Title in Titles:
        print(f'{counter}: {Title}')
        counter += 1
    answer = input('\nС каким тайтлом работаем? : ')
    if answer.isdigit() and int(answer) <= len(Titles):
        Title = Titles[int(answer) - 1]
        postmen = Telegraph_Postmen()
        postmen.Send_Title(Title)
    else:
        print('Error input')

    # print(postmen.Send_Post('Title', content=json.dumps([{'tag': 'img', 'attrs': {'src': src}},
    #                                                      {'tag': 'img', 'attrs': {'src': src}}])))
