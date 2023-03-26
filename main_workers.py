from uploader import Image_Upload
from config import BASE_PATH
import requests
import json
import os
import re


def Sort_Files(onlyFiles):
    onlyFiles.sort(key=lambda file: int(
        ''.join(re.findall('\d+', file.partition('.')[:1][0]))))


def Send_Title(title_name, Postmen_data):
    Files_Names = Get_Files_Names(title_name)
    Files_urls = []
    senders = []
    for file in Files_Names:
        senders.append(Image_Upload.delay(title=title_name, file=file))
    for sender in senders:
        sender.wait(timeout=None, interval=0.5)
        Files_urls.append({'tag': 'img', 'attrs': {'src': sender.get()}})
    return Send_Post(title_name, Files_urls, postmen_data=Postmen_data)


def Sort_Files(onlyFiles):
    onlyFiles.sort(key=lambda file: int(
        ''.join(re.findall('\d+', file.partition('.')[:1][0]))))


def Get_Files_Names(title, subtitle=None):
    if subtitle == None:
        osDir = f"{BASE_PATH}{title}/"
    else:
        osDir = f"{BASE_PATH}{title}/{subtitle}/"
    onlyFiles = [f for f in os.listdir(
        osDir) if os.path.isfile(os.path.join(osDir, f))]
    try:
        onlyFiles.remove('.DS_Store')
    except:
        pass
    Sort_Files(onlyFiles)
    return onlyFiles


def Send_Post(title_name, content, postmen_data):
    postmen_data['title'], postmen_data['content'] = title_name, content
    print(postmen_data)
    create_page = requests.post(
        'https://api.telegra.ph/createPage?', json=postmen_data)
    return json.loads(create_page.content)
