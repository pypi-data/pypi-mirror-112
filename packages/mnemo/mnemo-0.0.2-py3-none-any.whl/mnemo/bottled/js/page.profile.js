$(function () {
    $("a.edit-button").click(function (e) {
        e.preventDefault();
        let target_field = $(this).data("target-field");
        let new_value = prompt("New value for '" + target_field + "'");

        if ("email" == target_field) {
            if (!isEmail(new_value)) {
                alert("A proper email is required. Try again.");
                return;
            }
        }

        if (new_value != null) {
            $.post("/profile_edit_field",
                { "field": target_field, "value": new_value },
                function (data) {
                    if (data.success == true) {
                        location.reload();
                    } else {
                        console.log(data);
                    }
                }
            );
        }
    });
});