from main_workers import Send_Title
import os
import datetime
BASE_PATH = '/Users/sergejbaskakov/Desktop/Python/test_rq/src/'

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



if __name__ == "__main__":
    Titles = Get_Tiles()
    counter = 1
    for Title in Titles:
        print(f'{counter}: {Title}')
        counter += 1
    answer = input('\nС каким тайтлом работаем? : ')
    if answer.isdigit() and int(answer) <= len(Titles):
        Title = Titles[int(answer) - 1]
        time_start = datetime.datetime.now()
        result = Send_Title(Title)
        print(f'{result}\n\n{datetime.datetime.now() - time_start}')
    else:
        print('Error input')
