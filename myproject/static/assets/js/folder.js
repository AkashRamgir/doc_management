$(document).on('dblclick', '.folder_wrapper',function(){
    var id = $(this).parent().data('id')
    window.location = '/index/?parent_folder='+id
 })