$(function () {
    $("form#login").submit(function (e) {
        e.preventDefault();
        $.post('/login', $(this).serialize(), function (data) {
            if (data.success == true) {
                location.reload();
            } else {
                console.log(data);
            }
        },
            'json'
        );
    });
});