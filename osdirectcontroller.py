from config import BASE_PATH

import os
import re


def Get_Tiles():
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

# перебираем все файлы и удаляем txt


def Cleaning_Txt(onlyFiles, title):
    for file in onlyFiles:
        exFile = file.partition('.')[1:]
        exFile = exFile[0] + exFile[1]
        if exFile == '.txt':
            os.remove(f'{BASE_PATH}{title}\\{file}')
            onlyFiles.remove(file)

# Сортировка с ключом-функцией, которая разбивает на до и после точки, и из первой части достает только числа


def Sort_Files(onlyFiles):
    onlyFiles.sort(key=lambda file: int(
        ''.join(re.findall('\d+', file.partition('.')[:1][0]))))


def Sort_Dirs(onlyDirs):
    onlyDirs.sort(key=lambda file: int(''.join(re.findall('\d+', file))))


def Get_Files_Names(title, subtitle=None):
    if subtitle == None:
        osDir = f"{BASE_PATH}{title}\\"
    else:
        osDir = f"{BASE_PATH}{title}\{subtitle}\\"
    onlyFiles = [f for f in os.listdir(
        osDir) if os.path.isfile(os.path.join(osDir, f))]
    try:
        onlyFiles.remove('.DS_Store')
    except:
        pass
    Cleaning_Txt(onlyFiles, title)
    Sort_Files(onlyFiles)
    return onlyFiles


def Сhecking_for_Multipackages(Titles, Bol=False):
    exMultiTitles = []
    exSimpleTitles = []
    for title in Titles:
        if Get_Several_Dir_Files_Names(title)[0] != []:
            exMultiTitles.append(title)
        else:
            exSimpleTitles.append(title)
        # print('CFM title  : ', title)
        # Files_Names = Get_Files_Names(title)
        # print('CFM Files_Names  : ', Files_Names)
        # for file in Files_Names:
        #     if os.path.isdir(f"{BASE_PATH}{title}\{file}\\"):
        #         if Bol:
        #             print('CFM  not Bol : ', Bol)
        #             exMultiTitles.append(title)
        #         else:
        #             return True
        #         break
        #     if not title in exMultiTitles:
        #         exSimpleTitles.append(title)

    return [exMultiTitles, exSimpleTitles]


def Get_Several_Dir_Files_Names(title):
    mainDirs = [f for f in os.listdir(f"{BASE_PATH}{title}\\") if os.path.isdir(
        os.path.join(f"{BASE_PATH}{title}\\", f))]
    try:
        mainDirs.remove('.DS_Store')
    except:
        pass
    Sort_Dirs(mainDirs)
    subDirs = []
    for subDir in mainDirs:
        subDirs.append(Get_Files_Names(title, subDir))
    exList = []
    exList.append(mainDirs)
    exList.append(subDirs)
    return exList


def Csv_Save(all_urls):
    try:
        os.remove('.\Build\\file.txt')
    except:
        pass
    try:
        print(all_urls)
        with open(".\Build\\file.txt", "w") as output:
            output.write(str(all_urls))
    except Exception as e:
        print(repr(e))
