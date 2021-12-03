from datetime import datetime

def mainpage(SITE):
    current_datetime = datetime.now()
    print(current_datetime)
    print('/system/mainpage/mainpage.py')

    SITE.addHeadCode('<script src="https://api-maps.yandex.ru/2.1/?lang=ru_RU"></script>')
    SITE.addHeadCode('<script src="/files/oil_pipelines/2021-01/data.js"></script>')
    SITE.addHeadFile('/templates/system/css/mainpage.css')
    SITE.addHeadFile('/templates/system/js/mainpage.js')

    SITE.content = f'''
        <h1>Карта</h1>
        <div id="map"></div>
    '''
