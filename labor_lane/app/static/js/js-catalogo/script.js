$(document).ready(function(){
	
	// AGREGANDO CLASE ACTIVE AL PRIMER ENLACE ====================
	$('.category_list .category_item[category="all"]').addClass('ct_item-active');

	// FILTRANDO PRODUCTOS  ============================================

	$('.category_item').click(function(){
		var catProduct = $(this).attr('category');
		console.log(catProduct);

		// AGREGANDO CLASE ACTIVE AL ENLACE SELECCIONADO
		$('.category_item').removeClass('ct_item-active');
		$(this).addClass('ct_item-active');

		// OCULTANDO PRODUCTOS =========================
		$('.product-item').css('transform', 'scale(0)');
		function hideProduct(){
			$('.product-item').hide();
		} setTimeout(hideProduct,400);

		// MOSTRANDO PRODUCTOS =========================
		function showProduct(){
			$('.product-item[category="'+catProduct+'"]').show();
			$('.product-item[category="'+catProduct+'"]').css('transform', 'scale(1)');
		} setTimeout(showProduct,400);
	});

	// MOSTRANDO TODOS LOS PRODUCTOS =======================

	$('.category_item[category="all"]').click(function(){
		function showAll(){
			$('.product-item').show();
			$('.product-item').css('transform', 'scale(1)');
		} setTimeout(showAll,400);
	});



    // Agrega un escuchador de eventos para todos los botones "Aceptar"
    
	// Delegación de eventos para manejar clics en botones Aceptar y Cancelar
	$(document).on('click', '.boton', function() {
		var alerta = $(this).closest('.product-item').find('.alerta');
		var dataTitulo = $(this).data('titulo');
	
		if ($(this).hasClass('aceptar')) {
			// Configurar la alerta con el título y mostrarla
			alerta.find('p.titulo').text(dataTitulo);
			alerta.find('#fechaActual').val(getFechaActual());
			alerta.show();
		} else if ($(this).hasClass('cancelar')) {
			// Ocultar la alerta si se hace clic en Cancelar
			alerta.hide();
		}
	});
	
		// Función para obtener la fecha actual en formato YYYY-MM-DD
	function getFechaActual() {
			return new Date().toISOString().split('T')[0];
	}
	
	
	
	

});

