$(document).ready(()=> {

    $(document).on("click", ".show-tracks-btn",(e)=>{
        $.ajax({
            url: '/me/top/',
            type: 'GET',
            beforeSend: function(xhr){
              $('#loading-holder').show();
            },
            statusCode: {
                200: (resp)=>{
                    $('#loading-holder').hide();
                    $('#tracks-columns-holder').empty();
                    resp.forEach((track)=>{
                        let track_name = track['track_name'];
                        let album_name = track['album_name'];
                        let artists_name = track['artists_name'];

                        if (track_name.length > 40){
                            track_name = track_name.substr(0, 50) + '...'
                        }
                        if (album_name.length > 40){
                            album_name = album_name.substr(0, 30) + '...'
                        }
                        if (artists_name.length > 40){
                            artists_name = artists_name.substr(0, 30) + '...'
                        }

                        $('#tracks-columns-holder').append(`
                            <tr data-uri="${track['track_uri']}">
                              <td>${track_name}</td>
                              <td>${artists_name}</td>
                              <td>${album_name}</td>
                              <td colspan="2" style="text-align: center; padding: 0 .5rem;">
                                <a class="remove-btn-link">
                                    &times;
                                </a>
                              </td>
                            </tr>
                        `);

                        $('#tracks-list-holder').css('display', 'flex');
                        $('#share-btn').css('display', 'block');
                        $('#tracks-final-count').text(resp.length + ' Tracks to share');
                        $('#tracks-final-count').css('display', 'block');
                    })
                }
            }
        })
    });

    // this function will execute when user removes a track
    $(document).on("click", ".remove-btn-link", (e)=>{
        let trackRow = $(e.target).parents('tr');
        trackRow.fadeOut('slow').queue(()=>{
            trackRow.remove();

            let tracksCount = $('#tracks-columns-holder').children('tr').length;
            if (tracksCount == 0){
                $('#share-btn').hide();
                $('#tracks-list-holder').hide();
                $('#tracks-final-count').hide();
            } else {
                $('#tracks-final-count').text(tracksCount + ' Tracks to share');
            }

        });
    });

    // prepare share-btn to show loading
    function showLoading(){
        $('#share-btn span').hide();
        $('#share-btn img').show();
        $('#share-btn').addClass('show-share-btn-loading').addClass('disabled');
    }

    function hideLoading() {
        $('#share-btn span').show();
        $('#share-btn img').hide();
        $('#share-btn').removeClass('show-share-btn-loading').removeClass('disabled');
    }

    // show an alert with danger theme
    function showDangerAlert(text){
        let htmlText = `
        <div class="alert alert-danger alert-dismissible fade show custom-danger-alert" role="alert">
            ${text}
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        `;
        $('body').prepend(htmlText);
    }

    // when user clicks on `Share` button this function will get all present tracks and send them
    // to server to be saved as users top tracks playlist.
    $(document).on('click', '#share-btn', (e)=>{
        if (!$('#share-btn').hasClass('disabled')){  // btn is not in loading mode and we can send ajax
            let allPresentTracks = [];
            showLoading();
            $('#tracks-columns-holder').children('tr').each((index, element)=>{
               allPresentTracks.push($(element).data('uri'));
            });
            console.log(allPresentTracks)
            $.ajax({
                url: '/me/share/',
                type: 'POST',
                data: {'uris': JSON.stringify(allPresentTracks)},
                statusCode: {
                    409: (resp)=>{
                        let aTag = '<a target="_blank" href="' + resp.responseJSON['url'] + '">here</a>';
                        let message = 'You already have shared a playlist. Click ' + aTag + ' to see.';
                        showDangerAlert(message);
                        hideLoading();
                    },
                    201: (resp)=>{
                        window.location.replace(resp);
                    }
                }
            })
        }

    });
});