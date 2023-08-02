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

        $timestamp.text(formattedTime);
    });
}

updateTimestamps();





// connecting websocket to chat

let protocol = 'ws'



if (window.location.protocol === 'https:') {
    protocol = 'wss'
}
let room_id = $('#room-id').data('room-id')
const USER = $('#room-id').data('user')

let url = `${protocol}://${window.location.host}/ws/chat/${room_id}`

const chatSocket = new WebSocket(url);

chatSocket.onopen = function (e) {
    console.log('Connected to chat socket')
    console.log(e)
}

chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    if (data.type === 'message') {
        console.log(data)
        AddMessage(data.user, data.message)

    }
}



$('#chat-form').submit(function (e) {
    e.preventDefault();
    updateTimestamps();

    let message = $('#chat-input').val();
    this.reset()

    chatSocket.send(JSON.stringify({
        'message': message,
        'user': USER,
    }))



});



function AddMessage(user, message) {
    html = `    <div>
                <small> @${user},
                    <span data-time="${getCurrentUTCTimeFormatted()}" class="time-updated">
                    </span>
                </small>
                <p>
                    ${message}
                </p>
                <a href="{%url 'edit-msg' message.id %}">Edit</a>
                <a href="{%url 'delete-msg' message.id %}">Delete</a>

                <hr>
            </div>`

    $('#chat-messages').append(html)
    updateTimestamps();
    window.scrollTo(0, document.body.scrollHeight);

}


// Initial update

// Update timestamps every 10 seconds (adjust the interval as needed)
setInterval(updateTimestamps, 10000); // 10000 ms = 10 seconds
