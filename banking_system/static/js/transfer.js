function currency_conversion() {
    var koef;
    $.ajax({
        type: "GET",
        url: "conversion/",
        data: {
            'outgoing_account_num': $("#outgoing_account_num").val(),
            'incoming_account_num': $("#incoming_account_num").val(),
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
    var koef = currency_conversion();
    currency_2.value = currency_1.value * koef;
}

function conversion_second() {
    var koef = currency_conversion();
    currency_1.value = currency_2.value * koef;
}