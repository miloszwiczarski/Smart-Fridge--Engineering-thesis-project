$(document).on('submit', '#login-form', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/login',
        data: {
            password: $("#password-login").val(),
            email: $("#email-login").val()
        },
        success: function () {
            document.location.reload();
        }
    })
});

$(document).on('submit', '#create-account-form', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/register',
        data: {
            password: $("#password-register").val(),
            confirm_password: $("#confirm-password-register").val(),
            email: $("#email-register").val(),
            number: $("#number-register").val()
        },
        success: function () {
            document.location.reload();
        }
    })
});

$(document).on('submit', '#logout-form', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/logout',
        data: {
        },
        success: function () {
            document.location.reload();
        }
    })
});
