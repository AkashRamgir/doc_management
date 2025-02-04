$(document).ready(function(){
    $('.open_menu').on('click', function(){
        $('aside').removeClass('-translate-x-[100%]')
    })
    $('.close_menu').on('click', function(){
        $('aside').addClass('-translate-x-[100%]')
    })
})