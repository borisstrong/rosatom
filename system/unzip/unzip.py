import os
import shutil
import gzip

def unzip(SITE):
    print('PATH: /system/unzip/unzip.py')

    DIR = 'files/oil_pipelines'

    for el in os.walk(DIR):
        if el[2] == ['L2A.npy.gz']:
            gz_file = el[0] + '/L2A.npy.gz'
            npy_file = el[0] + '/L2A.npy'

            with gzip.open(gz_file, 'rb') as f_in:
                with open(npy_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            os.remove(gz_file)

    SITE.content = f'''
        <h1>Утилита распаковки файлов</h1>
        <div>Все файлы L2A.npy.gz -> L2A.npy распакованы</div>
    '''
