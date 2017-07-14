/* get the input file and send it to server to get the output
 * result */

/*
var open_file_btn = document.getElementById('open-file-btn');
open_file_btn.addEventListener('change', function(event) {

});
*/
    

// useful utilities
function getCookie(name) {
    var cookie_value = '';
    if (document.cookie && document.cookie !== '') {
	var cookies = document.cookie.split(';');
	for (var i = 0; i < cookies.length; i++) {
	    var cookie = cookies[i]; // jQuery.trim(cookies[i])
	    if (cookie.substring(0, name.length + 1) === (name + '=')) {
		cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
		break;
	    }

	}
    }
    return cookie_value;
}


var convert_file_btn = document.getElementById('convert-file-btn');
convert_file_btn.addEventListener('click', function(event) {
    // alert('click output file!');

    var open_file_btn = document.getElementById('open-file-btn');

    var files = open_file_btn.files;

    // TODO: more check
    if(files.length == 0) {
	alert('Input file must be seleted first!');
	return;
    }

    var output_file_type_radios = document.getElementsByName('output-file-type');

    var output_file_type_val = '';

    for (var i = 0; i < output_file_type_radios.length; i++) {
	if (output_file_type_radios[i].checked == true) {
	    output_file_type_val = output_file_type_radios[i].value;
	    break;
	}

    }
    
    // do the job
    console.log('Filename: ' + files[0].name);
    console.log('Type: ' + files[0].type);
    console.log('Size: ' + files[0].size + ' bytes');

    var form = new FormData();
    form.append('user-file-name', files[0].name);
    form.append('output-file-format', output_file_type_val);
    form.append('user-file', files[0]);

    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
	console.log('loaded complete.');	
    };

    var csrf_token = getCookie('csrftoken');

    xhr.open('POST', '/converter/', true);
    xhr.setRequestHeader('X-CSRFToken', csrf_token);
    xhr.onreadystatechange = function() {
	if (xhr.readyState == 4) {
	    if (xhr.status == 200) {
		
		console.log('Upload complete.')
		console.log('response: ' + xhr.responseText);
		alert('转化成功！');
		var div_output = document.getElementById('output-file-result');
		div_output.innerHTML = '<b>' + 'Download it here:' + '</b>' +
		    '<br>' + '<a href="' + xhr.responseText + '">Result File</a>';

		
	    }
	}

    };
    xhr.send(form);

});
