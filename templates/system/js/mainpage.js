ymaps.ready(init);

function init() {

    // Читаем json файл
    console.log(data)

    var myMap = new ymaps.Map("map", {
            center: [55.76, 37.64],
            zoom: 10
        }, {
            // searchControlProvider: 'yandex#search'
        }),

        // Создаем геообъект с типом геометрии "Точка".
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

        // Создаем прямоугольник с помощью вспомогательного класса.
        myRectangle = new ymaps.Rectangle([
            // Задаем координаты диагональных углов прямоугольника.
            [55.66, 37.60],
            [55.71, 37.69]
        ], {
            //Свойства
            hintContent: 'Меня перетаскивать нельзя!',
            balloonContent: 'Прямоугольник 1'
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
}
