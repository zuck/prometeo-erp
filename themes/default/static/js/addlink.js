function fixUrl(url) {
    var tokens = $.grep(url.split('/'), function(n) {
        return(n);
    });
    return '/' + tokens.join('/') + '/';
}

$(document).ready(function() {

    $('form span.add a').live('click', function(e) {

        var link_id = $(this).attr("id");
        var widget_id = $(this).parent().attr("id");
        var dialog_id = widget_id + "-dialog";
        var parent_id = $(this).closest(".ui-dialog-content").attr("id");
        var current_url = $(this).closest("form").attr("action");

        $(this).attr('disabled', true);

        $("#" + widget_id)
        .append('<div class="add-dialog" id="' + dialog_id +'"></div>')
        .children("#" + dialog_id)
        .load(fixUrl($(this).attr("href")) + " #main")
        .dialog({
            resizable: false,
            position: ["center", "top"],
            modal: true,
            width: 800,
            close: function(event, ui) {

                var root = "#main";
                if (parent_id)
                    root = "#" + parent_id + " #main";
                
                $(root + " #" + widget_id).load(fixUrl(current_url) + " #main #" + widget_id + " > *");
                $("#" + dialog_id).remove();
            }
        });

        $(".ui-dialog").find('.ui-dialog-titlebar').hide();

        $(this).attr("disabled", false);

        e.preventDefault();
    });
});
