from aiohttp import web
from system.mainpage import mainpage
from system.ajax import ajax
from system.unzip import unzip


def router(SITE):
    print('PATH: /system/system.py')

    if SITE.p[1] == 'auth':  # Если заход с формы
        return {'redirect': '/system/'}

    # Вызов функций по ключу
    functions = {
        '': mainpage.mainpage,
        'unzip': unzip.unzip,
        'get_date_ajax': ajax.get_date_ajax,
    }

    if (SITE.p[1] not in functions):
        raise web.HTTPNotFound()

    # Вызов функции из словаря
    return functions[SITE.p[1]](SITE)
