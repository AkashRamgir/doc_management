
$(document).ready(function () {  

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
