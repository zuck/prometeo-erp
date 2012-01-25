$(document).ready(function() {

    $(".ui-dialog form").live("submit", function(e) {

        var dlg = $(this).closest(".ui-dialog-content");
        var submit_input = $(e.target).find(".submit input");

        submit_input.attr("disabled", true);

        $.ajax({
            type: $(this).attr("method"),
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(data, status, xhr) {

                if (xhr.status == 278)
                    dlg.dialog("close");

                else if (xhr.readyState == 4)
                    $("#" + dlg.attr("id") + " #main").html($(data).find("#main").html());
            }
        });

        submit_input.attr("disabled", false);

        e.preventDefault();
    });

    $(".ui-dialog .cancel a").live("click", function(e) {

        $(this).attr("disabled", true);

        var dlg = $(this).closest(".ui-dialog-content");

        dlg.dialog("close");

        $(this).attr("disabled", false);

        e.preventDefault();
    });
});
