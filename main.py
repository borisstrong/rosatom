import time
import sys
import base64
from cryptography import fernet
import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
sys.path.append('classes')
sys.path.append('system')
from Site import Site
from system import system
from auth import auth


@aiohttp_jinja2.template('system/main.html')
async def system_r(request):
    # Админка
    print('===== SYSTEM =====')
    SITE = site(request)

    SITE.post = await request.post()  # Ждём получение файлов методом POST
    SITE.session = await get_session(request)

    SITE.auth = 1 if 'auth' in SITE.session else 0  # Статус авторизации - 1, если есть сессия

    # Авторизация на сайте
    if (SITE.auth == 0):
        r = auth.auth(SITE)
        # Обработка редиректа
        if r and 'redirect' in r:
            return web.HTTPFound(r['redirect'])
        return {'AUTH': SITE.auth, 'content': SITE.content, 'head': SITE.getHead()}

    r = system.router(SITE)

    # Обработка редиректа
    if r and 'redirect' in r:
        return web.HTTPFound(r['redirect'])
    
    # Обработка ajax
    if r and 'ajax' in r:
        return web.HTTPOk(text=r['ajax'])

    return {'AUTH': SITE.auth, 'content': SITE.content, 'head': SITE.getHead()}



def site(request):
    SITE = Site()
    # path = request.match_info.get('url', '')
    path = request.path
    SITE.path = path
    SITE.p = path[1:].split('/')
    i = len(SITE.p)
    while i < 7:
        SITE.p.append('')
        i += 1
    SITE.request = request
    return SITE



app = web.Application(client_max_size=1024**100)

# Установка сессий
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key))

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.add_routes([web.static('/lib', 'lib'),
                web.static('/templates', 'templates'),
                web.static('/files', 'files'),
                web.get('/system{url:.*}', system_r),  # Админка
                web.post('/system{url:.*}', system_r)])

if __name__ == '__main__':
    web.run_app(app, port=9999)










