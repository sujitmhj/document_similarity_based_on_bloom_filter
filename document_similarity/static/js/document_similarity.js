// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$("#calculate").click(function(e){

	var file1 = $("#file1").val();
	var file2 = $("#file2").val();

    var shingle_size = $("#shingle_size").val();
    var shingle_length = parseInt(shingle_size);
    if(file1.split(" ").length <shingle_length || file2.split(" ").length < shingle_length )
    {
        alert("Document size should be greater than shingle size");
        return;
    }

	$.post("/calculate-similarity/",{file1:file1,file2:file2,shingle_size:shingle_size},function(data){
		data = JSON.parse(data);
		// $("#percent_value").html(data.similarity+"%");
		// $("#result_modal").modal('show');
        $("#s_with").val(Math.round(data.s_with*1000)/1000);
        $("#s_without").val(Math.round(data.s_without*1000)/1000);
        // Math.round(data.s_with*1000)/1000

	});
});