$(document).ready(()=> {
    $('#delete-modal .btn-success').click((e) => {
        $.ajax({
            url: '/playlist/delete',
            type: 'DELETE',
            statusCode: {
                200: (resp) => {
                    window.location.replace(resp);
                }
            }
        });
    })

    // populate playlist edit input
    $('#edit-name-modal').on('shown.bs.modal', (e) => {
        let playlistCurrentName = $('#playlist-display-name').text();
        $('#edit-name-input').val(playlistCurrentName);
    });

    // send ajax to change the playlist's name
    $('#button-save-edit-name').click((e)=>{
        let playlistCurrentName = $('#edit-name-input').val();
        $.ajax({
            url: window.location.pathname.split('/')[2] + '/change-name',
            type: 'PUT',
            data: {'new_name': playlistCurrentName},
            success: (resp) => {
                $('#playlist-display-name').text(resp);
                $('#edit-name-modal').modal('hide');
            },
            fail: (resp) => {
                alert('something went wrong!')
            }
        })
    })
});