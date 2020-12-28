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
                    console.log(resp);
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

    // when user clicks on `Share` button this function will get all present tracks and send them
    // to server to be saved as users top tracks playlist.
    $(document).on('click', '#share-btn', (e)=>{
        let allPresentTracks = [];
        $('#tracks-columns-holder').children('tr').each((index, element)=>{
           allPresentTracks.push($(element).data('uri'));
        });
    });
});