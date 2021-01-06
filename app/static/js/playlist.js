$(document).ready(
    $('#delete-modal .btn-success').click((e)=>{
        $.ajax({
            url: '/playlist/delete',
            type: 'DELETE',
            statusCode: {
                200: (resp)=>{
                    window.location.replace(resp);
                }
            }
        })
    })
);