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

$(document).ready(function(){
    // Cuando se hace clic en "Añadir al carrito"
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();

        // Obtener el botón y desactivarlo temporalmente para evitar clics múltiples
        var button = $(this);
        button.prop('disabled', true);

        // Obtener el ID del producto y la URL desde los atributos
        var food_id = button.attr('data-id');
        var url = button.attr('data-url');

        // Mostrar en consola los valores obtenidos (opcional, para depuración)
        console.log('Food ID:', food_id, 'URL:', url);

        // Datos que se enviarán en la solicitud
        var data = {
            food_id: food_id
        }

        // Realizar la solicitud AJAX
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response){
                console.log(response);  // Mostrar la respuesta para depuración

                // Si la respuesta contiene el estado 'success', actualizar el carrito
                if (response.status === 'success') {
                    // Actualizar la cantidad del carrito
                    $('#cart_counter').html(response.cart_counter['cart_count']);

                    // Mostrar una notificación al usuario
                    Swal.fire('Añadido al carrito', '', 'success');
                } 
                else if (response.status === 'error') {
                    // Mostrar un mensaje de error en caso de que el servidor devuelva un error
                    Swal.fire('Error', response.message, 'error');
                } 
                else if (response.status === 'login_required') {
                    // Si se requiere iniciar sesión
                    Swal.fire('Por favor, inicia sesión para continuar', '', 'info').then(function(){
                        window.location = '/login';  // Redirigir al inicio de sesión
                    });
                }
                // Reactivar el botón al finalizar la operación
                button.prop('disabled', false);
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);  // Mostrar el error en consola

                // Manejar errores según el código de estado
                if (xhr.status == 404) {
                    Swal.fire('Error', 'Recurso no encontrado.', 'error');
                } else {
                    Swal.fire('Error', 'Algo salió mal. Inténtalo de nuevo.', 'error');
                }

                // Reactivar el botón en caso de error
                button.prop('disabled', false);
            }
        });
    });

    // Colocar la cantidad del artículo en el carrito al cargar la página
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#' + the_id).html(qty);
    });
});
