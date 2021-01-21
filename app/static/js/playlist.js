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
            statusCode: {
                200: (resp) => {
                    $('#playlist-display-name').text(resp);
                    $('#edit-name-modal').modal('hide');
                    $('#edit-name-modal .empty-name-error').hide();
                },
                400: (resp) => {
                    $('#edit-name-modal .empty-name-error').show();
                }
            }
        })
    })

    function showImportButtonLoading(){
        let importBtn = $('#import-playlist-btn');
        importBtn.disabled = true;
        importBtn.children('img').show();
        importBtn.children('span').hide();
        importBtn.addClass('show-loading-style');
    }

    function hideImportButtonLoading(){
        let importBtn = $('#import-playlist-btn');
        importBtn.disabled = false;
        importBtn.children('img').hide();
        importBtn.children('span').show();
        importBtn.removeClass('show-loading-style');
    }
    // import playlist
    $('#import-playlist-btn').click((e) => {
        let playlistId = window.location.pathname.split('/')[2];
        $.ajax({
            url: 'import/',
            type: 'POST',
            data: {'playlist_id': playlistId},
            beforeSend: () => {
                showImportButtonLoading();
            },
            statusCode: {
                201: (resp) => {
                    hideImportButtonLoading();
                },
                400: (resp) => {
                    let serverMessage = resp.responseJSON['message'];
                    let serverResponseElement = $('#server-message');
                    if(serverMessage == 'no items to add'){
                        serverResponseElement.text('Error! There is no tracks to add to your playlist');
                    } else if (serverMessage == 'no playlist id'){
                        serverResponseElement.text('Error! It seems web page is not loaded properly. Please refresh the page.');
                    }
                    serverResponseElement.show();
                    serverResponseElement.delay(4000).fadeOut();
                    hideImportButtonLoading()
                },
                401: () => {
                    hideImportButtonLoading();
                    let serverResponseElement = $('#server-message');
                    serverResponseElement.text('Please sign in first!');
                    serverResponseElement.show();
                    serverResponseElement.delay(4000).fadeOut();
                }
            },
        })
    })
});