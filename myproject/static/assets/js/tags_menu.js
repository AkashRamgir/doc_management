$(document).ready(function () {
    $('.select-tag').on('click', function () {
        const $submenu = $(this).find('.tag_sub_menu');
        $submenu.toggle(); // Toggle the submenu visibility

        // Prevent the submenu from closing when clicking inside it
        $submenu.on('click', function (e) {
            e.stopPropagation(); // Prevent the event from propagating to parent elements
        });
        
    })
    
    $('.tag_sub_menu').on('click', '.submenu-item', function (e) {
      
        $(this).closest('.tag_sub_menu').hide(); // Hide the submenu
    });

    $('.search_user').on('keyup', function() {
        let searchValue = $(this).val().toLowerCase().trim(); // Get the input value and normalize it
        $('.search_user_container').each(function() {
            let userName = $(this).text().toLowerCase().trim(); // Get the text inside the current <li>
            if (userName.includes(searchValue)) {
                $(this).show(); // Show the matching <li>
            } else {
                $(this).hide(); // Hide the non-matching <li>
            }
        });
    });

    $('.toggle_list_btn.active').prepend('<i class="fa-solid fa-check theme-green me-2 font-20"></i>');
})