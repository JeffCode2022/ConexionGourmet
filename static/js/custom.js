let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: {'country': ['pe']},
        }
    );
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();

    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    } else {
        // Obtener las coordenadas directamente del objeto `place`
        var latitude = place.geometry.location.lat();
        var longitude = place.geometry.location.lng();

        // Asignar las coordenadas a los campos ocultos
        $('#id_latitude').val(latitude);
        $('#id_longitude').val(longitude);

        // Mantener la dirección seleccionada en el input
        $('#id_address').val(place.formatted_address);
    }
}


