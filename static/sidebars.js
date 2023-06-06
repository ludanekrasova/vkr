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
   '1': ['Супермаркет', 'Магазин спиртных напитков', 'Кондитерский магазин', 'Магазин здоровой пищи'],
   '2': ['Парикмахерская', 'Спа салон', 'Ремонт обуви', 'Ремонт ювелирных изделий', 'Фото на документы'],
   '3': ['Ресторан', 'Кафе', 'Бар', 'Ночной клуб'],
   '4': ['Клиника', 'Стоматологическая клиника', 'Ветеринарная клиника'],
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

function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
}

department = getQueryVariable('department');

if (department) {

   var selectValue = department;
   var selectOption = getQueryVariable('branch').replace("+"," ");

   // Empty the target field
   $('#choices').empty();
   
   // For each chocie in the selected option
   for (i = 0; i < lookup[selectValue].length; i++) {
      // Output choice in the target field

      var selected = '';
      if (selectOption == lookup[selectValue][i]) {
          selected = ' selected'
      }

      $('#choices').append("<option value='" + lookup[selectValue][i] + "'"+selected+">" + lookup[selectValue][i] + "</option>");
   }
}


