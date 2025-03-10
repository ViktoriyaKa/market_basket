// когда html document готов (прорисован)
$(document).ready(function (){
	// ловим событие клика по кнопке добавить в корзину
	$(document).on("click", ".add-to-cart", function (e) {
		// блокируем его базовое действие
		e.preventDefault();

		// берем количесвто товаров из корзины
		var PrInCartCount = $("#prod-cart-count");
		var CartCount = parseInt(PrInCartCount.text() || 0);
		
		// получвем id товара из атрибутта data-product-id
		var product_id = $(this).data("product-id");

		// из атребутта href берем ссылку на контроллер django 
		var add_to_cart_url = $(this).attr("href");

		$.ajax({
			type: "POST",
			url: add_to_cart_url,
			data: {
				product_id: product_id,
				csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
			},

			success: function (data) {
				// successMessage.html(data.message);
				// successMessage.fadeIn(400);
				CartCount++;
				PrInCartCount.text(CartCount);
				// console.log("#nocart0-"+product_id);
				$("#cart0-"+product_id).hide();
				$("#cart1-"+product_id).show();
				if (data['last'] == true) {
					$("#prod_nolast-"+product_id).hide();
					$("#prod_last-"+product_id).show();
				} else {
					// console.log(ProductCount)
					$("#prod_nolast-"+product_id).show();
					$("#prod_last-"+product_id).hide();
				}

				// var PrInCartCount = $("#prod-cart-count");


			}
		})
	}
)

	$(document).on("click", ".cart-decr", function (ev) {
		// блокируем его базовое действие
		ev.preventDefault();

		// берем количесвто товаров из корзины
		var PrInCartCount = $("#prod-cart-count");
		var CartCount = parseInt(PrInCartCount.text() || 0);
		
		// получвем id товара из атрибутта data-product-id
		var product_id = $(this).data("product-id");

		// получаем количество товара текущее в корзине
		var ProductCartCount = $("#prod-count-"+product_id);
		var ProductCount = parseInt(ProductCartCount.text() || 0);
		// console.log(ProductCount)

		// из атребутта href берем ссылку на контроллер django 
		var decr_cart_url = $(this).attr("href");

		$.ajax({
			type: "POST",
			url: decr_cart_url,
			data: {
				product_id: product_id,
				csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
			},
			success: function (data) {
				// successMessage.html(data.message);
				// successMessage.fadeIn(400);
				CartCount--;
				PrInCartCount.text(CartCount);
				ProductCount--;
				// console.log(ProductCount)
				if (ProductCount > 0) {
					ProductCartCount.text(ProductCount);
					$("#prod_nolast-"+product_id).show();
					$("#prod_last-"+product_id).hide();
				} else {
					// console.log(ProductCount)
					$("#cart0-"+product_id).show();
					$("#cart1-"+product_id).hide();
				}

				// console.log("#nocart0-"+product_id);
				// $("#nocart0-"+product_id).hide();
				// $("#nocart1-"+product_id).show();

				// var PrInCartCount = $("#prod-cart-count");
			// console.log(data)


			}
		})
	}
)


	$(document).on("click", ".cart-inc", function (eve) {
		// блокируем его базовое действие
		eve.preventDefault();
		
		// берем количесвто товаров из корзины
		var PrInCartCount = $("#prod-cart-count");
		var CartCount = parseInt(PrInCartCount.text() || 0);
		
		// получвем id товара из атрибутта data-product-id
		var product_id = $(this).data("product-id");

		// получаем количество товара текущего в корзине
		var ProductCartCount = $("#prod-count-"+product_id);
		var ProductCount = parseInt(ProductCartCount.text() || 0);
		// console.log(product_id)
		// console.log(ProductCount)

		// из атребутта href берем ссылку на контроллер django 
		var decr_cart_url = $(this).attr("href");

		$.ajax({
			type: "POST",
			url: decr_cart_url,
			data: {
				product_id: product_id,
				csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
			},
			success: function (data) {
				// successMessage.html(data.message);
				// successMessage.fadeIn(400);
				// console.log(data['max']);
				if (data['max'] == false) {
					CartCount++;
					PrInCartCount.text(CartCount);
					ProductCount++;
					ProductCartCount.text(ProductCount);
				} 


				if (data['last'] == true) {
					$("#prod_nolast-"+product_id).hide();
					$("#prod_last-"+product_id).show();
				} else {
					// console.log(ProductCount)
					$("#prod_nolast-"+product_id).show();
					$("#prod_last-"+product_id).hide();
				}
				// console.log("#nocart0-"+product_id);
				// $("#nocart0-"+product_id).hide();
				// $("#nocart1-"+product_id).show();

				// var PrInCartCount = $("#prod-cart-count");
			// console.log(data)


			}
		})
	}
)

	// var PrInCartCount = $("#prod-cart-count");
	// var CartCount = parseInt(PrInCartCount.text() || 0);
	// // alert("A")
	// console.log(CartCount);
	// PrInCartCount.text("lol")
}

	)