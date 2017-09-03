function loading(){
	$("#loading").show();
	$("#content").hide();
	//setTimeout(function() { stop(); }, 10000);
}


/*$(document).ready(function() {

     $('form').on('submit', function(event) {

		$("#loading").show();
		$("#content").hide();

		$.ajax({

			data : {
				query : $('#query').val()
			},
			type : 'POST',
			url : '/'

		}).done(function(data) {

			$("#loading").hide();
			$("#content").show();

		});

	});

 });*/