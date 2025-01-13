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
    } )
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
            data:{folder_name : folder_name, parent_folder: parent_folder,user_id:user_id},
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

    // Modal for Update User 
    $('.update_user').on('click', function () { 
        const userId = $(this).data('user-id');
        if (userId) {
            $.ajax({
                url:"/get_user/",
                type:"POST",
                data:{userId : userId},
                headers: {
                    "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
                },
                success:function(data){
                     // Populate form fields with the received data
                    $('#updateUserForm #userId').val(data.id);
                    $('#updateUserForm #username').val(data.username);
                    $('#updateUserForm #email').val(data.email);
                    $('#updateUserForm #role').val(data.role);
                    $('#updateUserModal').modal('show');                  
                },
                error: function (xhr, status, error) {
                    console.error("Failed to fetch user data:", error);
                }
            })        
        } else {
            console.error("User ID is undefined!");
        }
    });

}) 