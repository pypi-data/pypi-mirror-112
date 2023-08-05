validate_new_password = function () {
    pwd1 = $("input#new_password").val();
    pwd2 = $("input#confirm_password").val();

    if (pwd1 == pwd2 && pwd1.length >= 8 && pwd1.length <= 20) {
        $("input#new_password").addClass("is-valid");
        $("input#confirm_password").addClass("is-valid");
        $("input#new_password").removeClass("is-invalid");
        $("input#confirm_password").removeClass("is-invalid");
        $("#password-edit-dialog input[type=submit]").removeClass("disabled");
    } else {
        $("input#new_password").removeClass("is-valid");
        $("input#confirm_password").removeClass("is-valid");
        $("input#new_password").addClass("is-invalid");
        $("input#confirm_password").addClass("is-invalid");
        $("#password-edit-dialog input[type=submit]").addClass("disabled");
    }
}

$(function () {
    $("#password-edit-form").submit(function (e) {
        e.preventDefault();
        $.post("/profile_edit_field",
            $(this).serialize(),
            function (data) {
                if (data.success == true) {
                    alert("Password changed!");
                    location.reload();
                } else {
                    console.log(data);
                }
            }
        );
    });

    $("input.new-password-fields").keyup(validate_new_password);

    $("a.change-password-dialog-trigger").click(function (e) {
        e.preventDefault();
        $("#password-edit-dialog").removeClass("d-none");
        $("#body-veil").removeClass("d-none");
    });

    $("#password-edit-dialog a.dialog-close-button").click(function (e) {
        e.preventDefault();
        $("#password-edit-dialog").addClass("d-none");
        $("#body-veil").addClass("d-none");
    });

});