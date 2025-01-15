
$(document).ready(function () {  

        $(document).ready(function () {
            $('#password').on('change', function () {
                const password = $(this).val(); // Get the password value
                const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
        
                if (!passwordRegex.test(password)) {
                    // Display the error message
                    $('#passwordError').text(
                        "Password must contain:\n" +
                        "- At least one uppercase letter\n" +
                        "- At least one lowercase letter\n" +
                        "- At least one number\n" +
                        "- At least one special character (@$!%*?&)\n" +
                        "- Be 8-16 characters long."
                    ).show();
                } else {
                    // Hide the error message
                    $('#passwordError').hide();
                }
            });
        });

        $('#addUserForm').on('submit', function (e) {
            e.preventDefault(); // Prevent the default form submission
            let email = $('#email').val();
            let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!emailPattern.test(email)) {
                alert("Please enter a valid email address.");
                return; // Stop form submission if email is invalid
            }
            let formData = new FormData(this);
            // Send AJAX request
            $.ajax({
                type: 'POST',
                url: "/save_users/", // URL for the new save_users view
                data: formData,
                processData: false,  // Important
                contentType: false,  // Important
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}' // CSRF token for security
                },
                success: function (response) {
                    if (response.status === 'success') {
                        alert(response.message); // Show success message
                        location.reload(); // Reload the page to reflect changes
                    } else {
                        alert('Error adding user.');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                }
            });
        });

        // On click of Update button get the user data:
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
                        console.log(full_name);
                        // Populate form fields with the received data
                        $('#updateUserForm #userId').val(data.id);
                        $('#updateUserForm #full_name').val(data.fullname);
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


        $('#updateUserForm').on('submit', function (e) {
            e.preventDefault(); // Prevent the default form submission
           
            let formData = new FormData(this);
            // Send AJAX request
            $.ajax({
                type: 'POST',
                url: "/update_user/", // URL for the new save_users view
                data: formData,
                processData: false,  // Important
                contentType: false,  // Important
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}' // CSRF token for security
                },
                success: function (response) {
                    if (response.status === 'success') {
                        alert(response.message); // Show success message
                        location.reload(); // Reload the page to reflect changes
                    } else {
                        alert('Error adding user.');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                }
            });
        });

        $(document).on('click', '.btn-sm[title="Delete User"]', function () {
            if (confirm('Are you sure you want to delete this user?')) {
                const userId = $(this).data('user-id'); // Get the user ID from the button's data attribute
                
                $.ajax({
                    type: 'POST',
                    url: '/delete_user/', // URL for the delete_user view
                    data: {
                        user_id: userId                
                    },
                    headers: {
                        'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'), // CSRF token for security
                    },
                    success: function (response) {
                        if (response.status === 'success') {
                            alert(response.message); // Show success message
                            location.reload(); // Reload the page to reflect changes
                        } else {
                            alert(response.message); // Show error message
                        }
                    },
                    error: function (xhr, status, error) {
                        console.error('Error:', error);
                        alert('An error occurred. Please try again.');
                    },
                });
            }
        });
});
