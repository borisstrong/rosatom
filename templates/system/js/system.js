document.addEventListener("DOMContentLoaded", ()=>{
	DAN.$('map_create').onclick = () => {
        let html = 
            '<h2>ВНИМАНИЕ!</h2>' +
            '<div>Потребуется обработка нескольких десятков тысяч файлов. Это очень долгий процесс.</div>' + 
            '<div style="margin-top:20px;text-align:center">' + 
                '<a id="map_create_start" class="dan_button_green" href="/system/map_create">Понятно, стартуем</a> ' + 
                '<span id="map_create_cancel" class="dan_button_gray">В другой раз</span>' +
            '</div>'
        DAN.modal.add(html)
        DAN.$('map_create_cancel').onclick = DAN.modal.del
    }
});