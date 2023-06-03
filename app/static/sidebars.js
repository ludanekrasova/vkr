/* global bootstrap: false */
(function () {
  'use strict'
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl)
  })
})()


// Map your choices to your option value
var lookup = {
   '1': ['Супермаркет', 'Магазин у дома', 'Магазин спиртных напитков', 'Кондитерский магазин', 'Магазин здоровой пищи'],
   '2': ['Парикмахерская', 'Салон красоты', 'Спа салон'],
   '3': ['Ресторан', 'Кафе', 'Бар', 'Ночной клуб'],
   '4': ['Бытовая химия', 'Магазин косметики', 'Магазин одежды'],
   '5': ['Клиника', 'Стоматологическая клиника', 'Ветеринарная клиника'],
   '6': ['Кофе на вынос', 'Ремонт обуви', 'Ремонт ювелирных изделий', 'Автомойка' , 'Фото на документы', 'Газетный киоск', 'Киоск мороженного', 'Химчистка'],
};

// When an option is changed, search the above for matching choices
$('#options').on('change', function() {
   // Set selected option as variable
   var selectValue = $(this).val();

   // Empty the target field
   $('#choices').empty();
   
   // For each chocie in the selected option
   for (i = 0; i < lookup[selectValue].length; i++) {
      // Output choice in the target field
      $('#choices').append("<option value='" + lookup[selectValue][i] + "'>" + lookup[selectValue][i] + "</option>");
   }
});
