$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData(document.getElementById('upload-file'));
		
        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                
				if(data == '[1]'){
					$('#result').text(' Result:  BAD' );
					$("#result").css("color", "red");
					console.log('Success1!');
				}
				if(data == '[2]'){
					$('#result').text(' Result:  GOOD' );
					$("#result").css("color", "green");
					console.log('Success2!');
				}
				if(data == '[0]'){
					$('#result').text(' Result:  Average' );
					$("#result").css("color", "Yellow");
					console.log('Success0!');
				}
				
            },
        });
    });

});