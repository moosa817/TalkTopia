$('.delete-btn').click(function (e) {
    let room_id = $(this).data('id')
    let room_name = $(this).data('name')
    $('#room-name').text(room_name)

    $('#confirm-delete-btn').data('id', room_id)
});

$('#confirm-delete-btn').click(function (e) {
    let room_id = $(this).data('id')
    let user = $('#current_user').data('user')
    let room_name = $('#room-name').text();

    token = $("#change_password-form").find('input[name=csrfmiddlewaretoken]').val()

    $.ajax({
        data: {
            user: user,
            room_id: room_id,
            csrfmiddlewaretoken: window.CSRF_TOKEN
        },
        type: 'POST',
        url: '/delete-room'
    })
        .done(function (data) {
            if (data.success) {
                $(`div[data-id=${room_id}]`).remove()
                $('#success').show()
                $('#mysuccess').text(`${room_name} room Removed`)


            }
        })

});