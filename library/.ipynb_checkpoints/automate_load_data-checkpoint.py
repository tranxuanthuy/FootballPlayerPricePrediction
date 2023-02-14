PATH_TO_PROJECT = '/home/thuy/Desktop/ML_project'
import sys
sys.path.append(PATH_TO_PROJECT)
from library import craw, preprocessing

def refresh_data():
    with open(PATH_TO_PROJECT + '/data/support/date.txt', 'r', encoding='utf-8') as fr:
        day = fr.readline()
    print(f'>>LATE UPDATED DATA ON {day}')
    print(':~$you want to continued?')
    while True:
        x = str(input(':~$you want to continued?:\n1 for yes, Rest for no'))
        if x != '1':
            break 
        else:
            print('>>Refress data')
            craw.automatic_dowload_raw_data()
            preprocessing.preprocess_data()
    if x != '1':
        print('>>Cancelled')

