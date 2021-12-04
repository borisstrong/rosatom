ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map("map", {
            // center: [55.76, 37.64],
            center: [data[0]['y1'], data[0]['x1']],
            zoom: 10
        }, {
            // searchControlProvider: 'yandex#search'
        })

        // Создаем геообъект с типом геометрии "Точка".
        /*
        myGeoObject = new ymaps.GeoObject({
            // Описание геометрии.
            geometry: {
                type: "Point",
                coordinates: [55.8, 37.8]
            },
            // Свойства.
            properties: {
                // Контент метки.
                iconContent: 'Я тащусь',
                hintContent: 'Ну давай уже тащи'
            }
        }, {
            // Опции.
            // Иконка метки будет растягиваться под размер ее содержимого.
            preset: 'islands#blackStretchyIcon',
            // Метку можно перемещать.
            draggable: true
        })
        */

    // Выбираем первые 100 bbox
    console.log(data)
    for (var i = 0; i < data.length; i++) {
        rect = new ymaps.Rectangle([
            // Задаем координаты диагональных углов прямоугольника.
            [data[i]['y1'], data[i]['x1']],
            [data[i]['y2'], data[i]['x2']]
        ], {
            //Свойства
            hintContent: data[i]['uid'],
            balloonContent: '<div class="yamps_but" onclick="MP.get_images_ajax(\'' + data[i]['uid'] + '\')">Посмотреть</div>'
        }, {
            // Опции.
            // Цвет и прозрачность заливки.
            fillColor: '#7df9ff',
            // Дополнительная прозрачность заливки..
            fillOpacity: 0.32,
            // Цвет обводки.
            strokeColor: '#0000FF',
            // Прозрачность обводки.
            strokeOpacity: 0.62,
            // Ширина линии.
            strokeWidth: 2,
        });

        myMap.geoObjects.add(rect)
    }

    /*
    myMap.geoObjects
        .add(myGeoObject)
        .add(myRectangle)
        .add(new ymaps.Placemark([55.826479, 37.487208], {
            balloonContent: '<div id="quadcopter">Точка взлёта квадрокоптера</div>'
        }, {
            preset: 'islands#governmentCircleIcon',
            iconColor: '#56db40'
        }))
        .add(new ymaps.Placemark([55.694843, 37.435023], {
            balloonContent: 'Розлив нефти',
            // iconCaption: 'Текст на карте'
        }, {
            preset: 'islands#redDotIconWithCaption'
        }))
        .add(new ymaps.Placemark([55.790139, 37.814052], {
            balloonContent: 'Розлив нефти',
            // iconCaption: 'Очень длиннный, но невероятно интересный текст'
        }, {
            preset: 'islands#redDotIconWithCaption',
            iconCaptionMaxWidth: '50'
        }));
    */
}

MP = {
    get_images_ajax(uid){
        console.log(uid)
        DAN.modal.spinner()
		let form = new FormData()
		form.append('uid', uid)
		DAN.ajax('/system/get_images_ajax', form, (data) => {
			console.log(data.imgs)
            let html = ''
            for (let i = 0; i < data.imgs.length; i++) {
                html += '<img class="yaml_img" src="' + data.imgs[i] + '">'
            }
            html = '<h2>Изображения в первом канале</h2><div class="dan_flex_row_start">' + html + '</div>'
            DAN.modal.add(html)
		})
    }
}
