//delete Msg 

let message_id;

$(document).on("click", ".delete-msg", function () {
    $('#delete-msg-btn').click()
    message_id = $(this).data('message-id')
    let a = $(`#msg-${message_id} p`)
    $('#msg-txt-modal').text(a.text())
})

$('#delete-btn-confirm').click(function (e) {
    $(`#msg-${message_id}`).fadeOut();
    $(`#msg-${message_id}`).remove();
    UpdateMsgIndex()
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
let message_id_edit;
let classes = "dark:bg-gray-800 bg-gray-200 border rounded"


$(document).on("click", ".edit-msg", function () {
    message_id_edit = $(this).parent().parent().parent().parent().parent().attr('id')

    $(`#msg-${message_id_edit} p`).attr('contenteditable', 'true')
    $(`#msg-${message_id_edit} p`).addClass(classes);
    $(`#msg-${message_id_edit} p`).focus();



    $(`#msg-${message_id_edit} .edit-done`).show()
    $(this).hide()


})
$(document).on('click', '.edit-done', function (e) {

    console.log(message_id_edit)

    $(`#${message_id_edit} p`).attr('contenteditable', 'false')
    $(`#${message_id_edit} p`).removeClass(classes);
    $(`#${message_id_edit} .edit-msg`).show()
    $(`#${message_id_edit} .edit-done`).hide()




    let msg_id = parseInt(message_id_edit.split('-')[1])
    let new_msg = $(`#${message_id_edit} p`).text().trim()

    console.log(msg_id, new_msg)
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
                return
            }
        })
})