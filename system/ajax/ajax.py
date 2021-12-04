import os
import shutil
import numpy as np
import json
import base64
from datetime import datetime
import matplotlib.pyplot as plt


def get_images_ajax(SITE):
    uid = SITE.post['uid']
    dir = 'files/oil_pipelines/2021-01/' + uid + '/sentinel2-l2a/patches/64x64-10/2021/data'
    path = dir + '/L2A.npy'
    imgs_np = np.load(path)

    imgs_list = []
    for i in range(imgs_np.shape[0]):
        img = imgs_np[i,0:64,0:64,0]
        file_path = dir + '/' + str(i) + '.jpg'
        plt.figure(figsize=(0.64, 0.64))
        plt.axis('off')
        plt.imshow(img, cmap='gray')
        plt.savefig(file_path)
        imgs_list.append('/' + file_path)

    answer = {'answer': 'success', 'imgs': imgs_list}
    return {'ajax': json.dumps(answer)}