function currency_conversion(сur_name_1, cur_name_2) {
    var koef;
    $.ajax({
        type: "GET",
        url: "conversion/",
        data: {
        },
        dataType: "text",
        cache: false,
        success: function(data) {
            koef = parseFloat(data);
        }
    })
    alert("Конвертация прошла успешно");
    return koef;
}

function conversion_first() {
    var koef = currency_conversion('RUB', 'EUR');
    currency_2.value = currency_1.value * koef;
}

function conversion_second() {
    var koef = currency_conversion('EUR', 'RUB');
    currency_1.value = currency_2.value * koef;
}