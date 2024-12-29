//delete Msg 

let message_id;

$(document).on("click", ".delete-msg", function () {

    $('#delete-msg-btn').click()
    message_id = $(this).parent().parent().parent().parent().parent().attr('id').split('-')[1];
    let a = $(`#msg-${message_id} p`)
    $('#msg-txt-modal').text(a.text())
})

$('#delete-btn-confirm').click(function (e) {
    $(`#msg-${message_id}`).fadeOut();
    $(`#msg-${message_id}`).remove();

    $.ajax({
        data: {
            pk: message_id,
            csrfmiddlewaretoken: window.CSRF_TOKEN
        },
        type: 'POST',
        url: '/delete-msg'
    })
        .done(function (response) {
        })
})


//edit message 
let classes = "dark:bg-gray-800 bg-gray-200 border rounded"


$(document).on("click", ".edit-msg", function () {

    let message_id_edit = $(this).closest('[id^="msg-"]').attr('id').split('-')[1];

    $(`#msg-${message_id_edit} p`).attr('contenteditable', 'true')
    $(`#msg-${message_id_edit} p`).addClass(classes);
    $(`#msg-${message_id_edit} p`).focus();



    $(`#msg-${message_id_edit} .edit-done`).show()
    $(this).hide()


})
$(document).on('click', '.edit-done', function (e) {


    let message_id_edit = $(this).closest('[id^="msg-"]').attr('id').split('-')[1];
    $(`#msg-${message_id_edit} p`).attr('contenteditable', 'false')
    $(`#msg-${message_id_edit} p`).removeClass(classes);
    $(`#msg-${message_id_edit} .edit-msg`).show()
    $(`#msg-${message_id_edit} .edit-done`).hide()




    let msg_id = parseInt(message_id_edit)
    let new_msg = $(`#msg-${message_id_edit} p`).text().trim()

    $.ajax({
        data: {
            msg_id: msg_id,
            new_msg: new_msg,
            csrfmiddlewaretoken: window.CSRF_TOKEN
        },
        type: 'POST',
        url: '/edit-msg'
    })
        .done(function (response) {
            if (response.success) {
                $(`#msg-${message_id_edit} .is-edited`).text('(edited)')
            }
        })
})