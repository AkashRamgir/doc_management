$(document).ready(function () {
    $('.new_folder_modal').on('click', function () {
        $('.folder_modal').modal('show')
    })
    $('#folder_name').on('keyup',function(){
        if($(this).val() == ''){
            $('.create_folder').prop('disabled', true)
        }else{
            $('.create_folder').prop('disabled', false)
        }
    })
    $('.create_folder').on('click', function(){
        $('.folder_modal').modal('hide')
        var folder_name = $('#folder_name').val();
        var parent_folder = $('#parent_folder_id').val();
        var user_id = $('#user').val();
        if(folder_name == ""){
           alert('Folder Name is blank') 
           return
        }
        $.ajax({
            url:"/create_folder/",
            type:"POST",
            data:{folder_name : folder_name, parent_folder: parent_folder, user_id: user_id},
            headers: {
                "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
            },
            success:function(html){
                $('.toast').toast('show')
            }
        })
    })
    $('.folder_modal').on('hidden.bs.modal', function(){
        $('.folder_modal').find('#folder_name').val('Untitled folder')
    })

    $('.modal-show').on('click', function(){
        $('.toast').css('bottom', '0');
    })
})

// Modal for File Upload Function
function handleFileUpload(){
    alert('File Upload Started')
    $('#fileUpload').submit()
}

// File upload AJAX success handler
$('#fileUpload').on('submit', function (e) {
    e.preventDefault(); // Prevent the default form submission

    // Get the file from the form input
    var fileInput = $('#fileUpload input[type="file"]')[0];
    var file = fileInput.files[0];

    console.log('File Selected:', file);
    console.log('File Type:', file.type);

    // Define the allowed file types (matching with the ALLOWED_FILE_TYPES in files.py)
    var allowedTypes = [
        'application/pdf',   // .pdf files
        'image/jpeg',         // .jpeg, .jpg files
        'image/png',          // .png files
        'image/gif',          // .gif files
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // .docx files
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',    // .xlsx files
        'application/vnd.openxmlformats-officedocument.presentationml.presentation', // .pptx files
        'text/plain',         // .txt files
        'video/mp4',          // .mp4 files
        'video/avi',          // .avi files
        'video/quicktime',    // .mov files
        'video/x-matroska',   // .mkv files
        'video/x-flv',        // .flv files
        'video/webm',         // .webm files
        'application/zip',    // .zip files
        'application/x-zip-compressed', // .zip files (alternate MIME type)
        'application/x-rar-compressed', // .rar files
        'application/x-tar',  // .tar files
        'application/gzip'    // .gz files
    ];

    // Check if the file type is allowed
    if (file && allowedTypes.indexOf(file.type) === -1) {
        console.error('Unsupported file type:', file.type);
        alert('Unsupported file type. Please upload a valid file.');
        return; // Stop the form submission
    }

    // Proceed with the AJAX file upload if the file is valid
    var formData = new FormData(this); // Get the form data

    $.ajax({
        url: '/upload_file/', // Adjust the URL to where the file should be uploaded
        type: 'POST',
        data: formData,
        processData: false, // Required for FormData
        contentType: false, // Required for FormData
        headers: {
            "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
        },
        success: function (response) {
            // Handle the success response
            alert('File Uploaded Successfully'); // Display the success alert box here
        },
        error: function (xhr, status, error) {
            console.error("File upload failed:", error);
            alert('File Upload Failed');
        }
    });
});
