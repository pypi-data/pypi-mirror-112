validate_first_email = function () {
    email1 = $("#user_email").val();
    email2 = $("#email_confirmation").val();

    validated = email1 == email2 && isEmail(email1) && isEmail(email2)

    if (validated) {
        $("form#first-setup input[type=email]").addClass("is-valid");
        $("form#first-setup input[type=email]").removeClass("is-invalid");
    } else {
        $("form#first-setup input[type=email]").removeClass("is-valid");
        $("form#first-setup input[type=email]").addClass("is-invalid");
    }

    return validated
}

validate_first_password = function () {
    pwd1 = $("#user_password").val();
    pwd2 = $("#password_confirmation").val();

    validated = pwd1 == pwd2 && pwd1.length >= 8 && pwd1.length <= 20;

    if (validated) {
        $("form#first-setup input[type=password]").addClass("is-valid");
        $("form#first-setup input[type=password]").removeClass("is-invalid");
    } else {
        $("form#first-setup input[type=password]").removeClass("is-valid");
        $("form#first-setup input[type=password]").addClass("is-invalid");
    }

    return validated
}

validate_first_form = function () {
    email_validated = validate_first_email();
    password_validated = validate_first_password();
    if (email_validated && password_validated) {
        $("form#first-setup button[type=submit]").removeClass("disabled");
    } else {
        $("form#first-setup button[type=submit]").addClass("disabled");
    }
    return email_validated && password_validated
}

$(function () {
    $("#user_email").keyup(validate_first_form);
    $("#email_confirmation").keyup(validate_first_form);
    $("#user_password").keyup(validate_first_form);
    $("#password_confirmation").keyup(validate_first_form);

    $("form#first-setup").submit(function (e) {
        if (validate_first_form() === false) {
            e.preventDefault();
            e.stopPropagation();
        } else {
            e.preventDefault();
            $.post('/first_setup', $(this).serialize(), function (data) {
                if (data.success === true) {
                    location.reload();
                } else {
                    console.log(data);
                }
            },
                'json'
            );
        }
    });
});