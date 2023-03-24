from celery import Celery
from uploader import Image_Upload
import os
import re

main_workers = Celery('main_workers', backend='redis://localhost',  broker='redis://localhost')

BASE_PATH = '/Users/sergejbaskakov/Desktop/Python/test_rq/src/'

def Sort_Files(onlyFiles):
    onlyFiles.sort(key=lambda file: int(
        ''.join(re.findall('\d+', file.partition('.')[:1][0]))))


@main_workers.task
def Send_Title(title):
    Files_Names = Get_Files_Names(title)
    print(Files_Names)
    Files_urls = []
    src = []
    for file in Files_Names:
        src.append(Image_Upload.delay(title=title, file=file))
    for tasks in src:
        tasks.wait(timeout=None, interval=0.5)
        Files_urls.append(tasks.get())
    return Files_urls


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
