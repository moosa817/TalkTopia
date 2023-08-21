// On page load or when changing themes, best to add inline in `head` to avoid FOUC
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark')
} else {
    document.documentElement.classList.remove('dark')
}

// Whenever the user explicitly chooses light mode
localStorage.theme = 'light'

// Whenever the user explicitly chooses dark mode
localStorage.theme = 'dark'

// Whenever the user explicitly chooses to respect the OS preference
localStorage.removeItem('theme')






//blur background when modal is opened
// $('.modal-btn').click(function (e) {
//     $('body').css('filter', 'blur(5px)')

// });
// Close the modal when clicking outside of it


$('.modal-btn').click(function () {
    $('#content').addClass('blurPage');
});

$('.modal-close').click(function () {
    $('#content').removeClass('blurPage');
})


const modals = $('.blur-modal')

window.addEventListener("click", (event) => {
    $.each(modals, function (indexInArray, modal) {
        if (event.target === modal) {
            $('#content').removeClass('blurPage');
        }
    });
});
$(document).keyup(function (e) {
    if (e.key === "Escape") { // escape key maps to keycode `27`
        $('#content').removeClass('blurPage');

    }
});



//topic btn
$(document).ready(function () {
    $("#topics a").each(function () {
        if ($(this).attr('href') == '/' + window.location.search) {
            $(this).css("background", "orange !important");
            $(this).find('div.the-btn').removeClass('trans-btn');
            $(this).find('div.the-btn').addClass('trans-btn-full');
        }
    });
});