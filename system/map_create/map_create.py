import os
import pandas as pd
import yaml
import json
from pathlib import Path
from eolearn.core import EOPatch

def map_create(SITE):
    print('PATH: /system/map_create/map_create.py')

    DIR = 'files/oil_pipelines'

    with open(DIR+'/patches.yaml') as fh:
        read_data = yaml.safe_load(fh)

    '''
    for dir_name in DIR:
        if (os.path.isdir(DIR + '/' + dir_name)):
            get_df(dir_name)  # Формируем json файлы и датафреймы
    '''
    get_df('2021-01')

    SITE.content = f'''
        <h1>Утилита создания объектов карты из файлов</h1>
        <div>JSON файлы были созданы</div>
    '''

# Функция получения датасета карты по наименованию папки 
def get_df(dir_name):
    print('PATH: /system/map_create/map_create.py -> get_df')

    DIR = 'files/oil_pipelines'

    with open(DIR + '/patches.yaml') as fh:
        read_data = yaml.safe_load(fh)

    result_list = []
    i = 0
    for yaml_el in read_data['patches']:
        for path_el in os.walk(DIR + '/' + dir_name + '/' + yaml_el['uid']):
            if path_el[1] == ['data', 'mask'] or path_el[1] == ['mask', 'data']:
                print(i, yaml_el['uid'])
                eopatch = EOPatch.load(path_el[0], lazy_loading=True)
                bbox = list(eopatch['bbox'])
                dct = {
                'uid':yaml_el['uid'],
                'lat':yaml_el['lat'],
                'lng':yaml_el['lng'],
                'x1':bbox[0],
                'y1':bbox[1],
                'x2':bbox[2],
                'y2':bbox[3],
                'status':0
                }
                result_list.append(dct)
                i += 1
    df = pd.DataFrame(result_list)
    df.head()
    df.to_csv(DIR + '/' + dir_name+'/df_for_map.csv')
    json_str = json.dumps(result_list)
    with open(DIR + '/' + dir_name+'/data.json', 'w') as f:
        json.dump(json_str, f) 
    return result_list