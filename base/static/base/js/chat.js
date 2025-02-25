$('#content').fadeOut();
$('#load-div').fadeIn();

//for time stamps

function getCurrentUTCTimeFormatted() {
    const now = new Date();
    const year = now.getUTCFullYear();
    const month = String(now.getUTCMonth() + 1).padStart(2, '0');
    const day = String(now.getUTCDate()).padStart(2, '0');
    const hours = String(now.getUTCHours()).padStart(2, '0');
    const minutes = String(now.getUTCMinutes()).padStart(2, '0');
    const seconds = String(now.getUTCSeconds()).padStart(2, '0');
    const formattedTime = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}Z`;
    return formattedTime;
}


function updateTimestamps() {
    const now = new Date();

    $('.time-updated').each(function () {
        const $timestamp = $(this);
        const timestampText = $timestamp.attr('data-time');
        const timestamp = new Date(timestampText);

        // Calculate the time difference in seconds
        const diffInSeconds = Math.floor((now - timestamp) / 1000);

        // Calculate the time difference in various units
        const secondsInMinute = 60;
        const secondsInHour = 60 * secondsInMinute;
        const secondsInDay = 24 * secondsInHour;
        const secondsInWeek = 7 * secondsInDay;
        const secondsInMonth = 30 * secondsInDay; // Assuming 30 days per month
        const secondsInYear = 365 * secondsInDay; // Assuming 365 days per year

        let formattedTime;

        if (diffInSeconds >= secondsInYear) {
            const years = Math.floor(diffInSeconds / secondsInYear);
            formattedTime = `${years} year${years !== 1 ? 's' : ''} ago`;
        } else if (diffInSeconds >= secondsInMonth) {
            const months = Math.floor(diffInSeconds / secondsInMonth);
            formattedTime = `${months} month${months !== 1 ? 's' : ''} ago`;
        } else if (diffInSeconds >= secondsInWeek) {
            const weeks = Math.floor(diffInSeconds / secondsInWeek);
            formattedTime = `${weeks} week${weeks !== 1 ? 's' : ''} ago`;
        } else if (diffInSeconds >= secondsInDay) {
            const days = Math.floor(diffInSeconds / secondsInDay);
            formattedTime = `${days} day${days !== 1 ? 's' : ''} ago`;
        } else if (diffInSeconds >= secondsInHour) {
            const hours = Math.floor(diffInSeconds / secondsInHour);
            formattedTime = `${hours} hour${hours !== 1 ? 's' : ''} ago`;
        } else if (diffInSeconds >= secondsInMinute) {
            const minutes = Math.floor(diffInSeconds / secondsInMinute);
            formattedTime = `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
        } else {
            formattedTime = `${diffInSeconds} second${diffInSeconds !== 1 ? 's' : ''} ago`;
        }
        if (diffInSeconds <= 0) {
            formattedTime = 'Just now';
        }
        $timestamp.text(formattedTime);
    });
}

updateTimestamps();





// connecting websocket to chat


let room_id = $('#room-id').data('room-id')
const USER = $('#room-id').data('user')
const PFP = $('#room-id').data('pfp')



let url = window.WS_URL + '?room=' + room_id


const chatSocket = new ReconnectingWebSocket(url);

chatSocket.onopen = function (e) {
    console.info('Connected to chat socket')
    // one sec sleep
    setTimeout(function () {
        $('#content').fadeIn();
        $('#load-div').fadeOut();
        window.scrollTo(0, document.body.scrollHeight);

    }, 1000)

}

chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);

    if (data.type === 'edit') {
        let msg_id = data.msg_id
        let new_msg = data.new_msg

        $(`#msg-${msg_id} .msg-paragraph`).text(new_msg)
        $(`#msg-${msg_id} .is-edited`).text('(edited)')
    }

    if (data.type === 'delete') {
        let msg_id = data.msg_id
        $(`#msg-${msg_id}`).remove()
    }

    if (data.type === 'message') {

        let no = parseInt($('.counter').last().attr('id'))
        if (!no) {
            no = 0
        }
        no = no + 1

        let CurrentUser
        if (data.user == USER) {
            CurrentUser = true
        }

        let no_list = $('.counter').map(function () {
            return parseInt($(this).attr('id'));
        }).get();


        if (no_list.includes(data.msg_no)) {
            $(`#${data.msg_no}`).removeClass('opacity-50')
            $(`#${data.msg_no} #msg-null`).attr('id', `msg-${data.id}`)
            return
        }
        AddMessage(data.user, data.message, data.id, CurrentUser, data.edited, data.TimeUpdated, data.pfp, no, load = false, sent = true)

    }
}


$('#chat-form').keydown(function (e) {

    if (e.keyCode == 13) {
        let btn = document.getElementById('send-msg-btn')

        btn.click()
        window.scrollTo(0, document.body.scrollHeight);

    }
});
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

$('#chat-form').submit(function (e) {
    e.preventDefault();


    // reason without focusing outside message, message is null 
    let r = document.getElementById('rf')
    r.focus()
    updateTimestamps();
    let message = $('#chat-input').val();

    $('.emojionearea-editor').focus()


    this.reset()
    $('.emojionearea-editor').text('')
    if (message == "") {

    } else {

        let no = parseInt($('.counter').last().attr('id'))
        if (!no) {
            no = 0
        }
        no = no + 1

        AddMessage(USER, message, message_id = null, USER, edited = false, getCurrentUTCTimeFormatted(), PFP, no)


        chatSocket.send(JSON.stringify({
            'action': 'sendMessage',
            'message': message,
            'user_id': USER_ID,
            'room': room_id.toString(),
            'sessionid': getCookie('sessionid'),
            'msg_no': no
        }))
    }

});

function AddMessage(user, message, message_id, CurrentUser, edited, TimeUpdated, pfp, no, load = false, sent = false) {
    let btn, edited_html;
    if (edited) {
        edited_html = `(edited)`;
    } else {
        edited_html = '';
    }

    if (CurrentUser) {
        btn = `  <button class="mx-2 edit-msg"><i
        class="fa-pen fa-solid text-xs md:text-base"></i></button>

                <button class="mx-2 edit-done hidden"><i
                        class="fa-check fa-solid text-xs md:text-base"></i></button>
                <button class="delete-msg" data-modal-target="deleteMsg" data-modal-toggle="deleteMsg"><i
                        class="fa-trash text-xs md:text-base text-red-700 fa-solid"></i></button>`;
    } else {
        btn = '';
    }

    // Add a CSS class for unsent messages
    const sentClass = sent ? '' : 'opacity-50'; // Less opacity if not sent

    html = `<div class="counter ${sentClass}" id="${no}">
         <div id="msg-${message_id}">
            <div class="w-full my-4 flex justify-between">
                <div class="w-[14vw] min-[400px]:w-[10vw] sm:w-[8vw] md:w-[6vw] lg:w-[5vw] mr-1 ">
                    <a href="/profile/${user}"><img src="${pfp}" alt="img"
                            class="md:w-12 md:h-12 w-10 h-10 shadow-xl rounded-full object-cover">
                    </a>
                </div>
                <div class="w-[85vw] sm:w-[92vw] md:w-[94vw]">
                    <div class="flex justify-between">
                        <div>
                            <small> <a href="profile/${user}">@${user}</a>,
                                <span data-time="${TimeUpdated}"
                                    class="time-updated opacity-70 text-xs"></span>
                                <span class='is-edited text-xs opacity-50'>
                                    ${edited_html}
                                </span>
                            </small>
                            <p class="msg-paragraph" style="word-wrap:break-word;word-break: break-word;">
                                ${message}
                            </p>
                        </div>
                        <div class="flex">
                            ${btn}
                        </div>
                    </div>
                </div>
            </div>
            <hr class="h-px mt-1 bg-gray-100 border-0 dark:bg-gray-700">
        </div>
    </div>`;

    if (load) {
        $('#chat-messages').prepend(html);
    } else {
        $('#chat-messages').append(html);
    }

    updateTimestamps();
    window.scrollTo(0, document.body.scrollHeight);
}



// Initial update

// Update timestamps every 10 seconds (adjust the interval as needed)
setInterval(updateTimestamps, 20000); // 10000 ms = 10 seconds


//style for chat 
//toggle participants 
$('#toggle-participants').click(function () {
    $('#participants').toggle();


    if ($('#msg-container').hasClass('w-[80vw]') || $('#msg-container').hasClass('md:w-[80vw]')) {
        $('#msg-container').removeClass('md:w-[80vw]');
        $('#msg-container').addClass('w-[100vw]');
    }
    else {
        $('#msg-container').removeClass('w-[100vw]');
        $('#msg-container').addClass('md:w-[80vw]');

    }
    if ($('#chat-div').hasClass('md:w-[85%]')) {

        $('#chat-div').removeClass('md:w-[85%]');


    } else {
        $('#chat-div').addClass('md:w-[85%]');

    }


})


$('#toggle-participants-mobile').click(function () {
    $('#participants').toggle();
})



$(".emojionearea").emojioneArea({
    searchPlaceholder: "Search",
});



$('#leave').click(function () {
    $('#room-name-leave').text($('#current_room').text())

    // $(this).hide()
    // $('#join').show()
})


$('#join').click(function () {
    $.ajax({
        type: "GET",
        url: `/join_room?id=${room_id}`,
        dataType: "",
        success: function (response) {
            if (response.success) {
                $('#join').hide()
                $('#leave').removeClass('hidden');
                $('#leave').addClass('inline-flex');

                $('#participants-members').prepend(`<div class="py-2 mx-1 text-center font-extralight text-sm opacity-80">
                            <a href="/profile/${USER}">
                                ${USER}
                            </a>
                        </div>
                        <hr class="h-px bg-gray-100 border-0 dark:bg-gray-700">`
                );
            }
        }
    });

})
let invite_link = `${window.location.origin}/invite/${$('#CopyDropDownBtn').data('link')}`
$('#input-group-search').val(invite_link)


function CopywithJquery(element_id) {
    var temp = $("<input>");
    $("body").append(temp);
    temp.val($(element_id).val()).select();
    document.execCommand("copy");
    temp.remove();
}


$('#copy-invite-link').click(function () {
    $(this).text("Copied")

    CopywithJquery('#input-group-search')
    $('#input-group-search').select()
})




$(document).on('keypress', '.msg-paragraph', function (e) {
    if (e.keyCode === 13) {
        $('.edit-done').click()
    }
})

$(document).on('keypress', '.msg-paragraph', function (e) {
    return e.which != 13;

})


$('#loadmore').click(function (e) {
    let last_msg_no = parseInt($('.counter').last().attr('id'))
    $.ajax({
        data: {
            last_msg_no: last_msg_no,
            room_id: room_id,
            csrfmiddlewaretoken: window.CSRF_TOKEN
        },
        type: 'POST',
        url: '/load_messages'
    })
        .done(function (data) {
            if (data.length == 0) {
                $('#loadmore-center').html("<span class='opacity-50 text-xs'>Beginning of Room</span>")

                $('#loadmore').remove()
            }
            data.forEach(message => {
                AddMessage(message.username, message.body, message.id, message.CurrentUser, message.edited, message.created, message.pfp, '1', load = true, edited = message.edited)
                UpdateMsgIndex()
                window.scrollTo(0, 0);



            });
        })



})




