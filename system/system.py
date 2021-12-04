from aiohttp import web
from system.mainpage import mainpage
from system.ajax import ajax
from system.unzip import unzip
from system.map_create import map_create
from system.example_prediction import example_prediction


def router(SITE):
    print('PATH: /system/system.py')

    if SITE.p[1] == 'auth':  # Если заход с формы
        return {'redirect': '/system/'}

    # Вызов функций по ключу
    functions = {
        '': mainpage.mainpage,
        'unzip': unzip.unzip,
        'map_create': map_create.map_create,
        'get_images_ajax': ajax.get_images_ajax,
        'example_prediction': example_prediction.example_prediction
    }

    if (SITE.p[1] not in functions):
        raise web.HTTPNotFound()

    # Вызов функции из словаря
    return functions[SITE.p[1]](SITE)
