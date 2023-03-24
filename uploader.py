from celery import Celery
import requests
import json

uploader = Celery('uploader', backend='redis://localhost',  broker='redis://localhost')

BASE_PATH = '/Users/sergejbaskakov/Desktop/Python/test_rq/src/'

@uploader.task
def Image_Upload(title, file):
    path_to_file = f'{BASE_PATH}{title}/{file}'
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
