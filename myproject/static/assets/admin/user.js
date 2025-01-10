
$(document).ready(function () {  

        $('#addUserForm').on('submit', function (e) {
            e.preventDefault(); // Prevent the default form submission
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
});
