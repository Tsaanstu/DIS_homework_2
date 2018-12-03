function currency_conversion(id, cost) {
    $.ajax({
        type: "POST",
        url: "change_of_rate/",
        data: {
            'id': id,
            'cost': cost,
        },
        dataType: "text",
        cache: false,
        success: function(data) {

        }
    })
}


(function(){ document.addEventListener('DOMContentLoaded', function() {
    var but = document.querySelectorAll('.rate_btn');
		for(var i=0; i<but.length; i++) {
			but[i].onclick = function(event) {
				if(confirm("Обновить?")) {
				    console.log(this.id)
				    console.log(document.getElementsByName('InputCost')[this.id - 1].value)
                    currency_conversion(this.id, document.getElementsByName('InputCost')[this.id - 1].value)
				} else{
					event.preventDefault();
				}
			}
		}
});})();