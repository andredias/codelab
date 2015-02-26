"use strict";

(function ($) {

    var toggleSiblingDiv = function () {
        var parent = $(this).parents('div')[0];
        $(parent).toggleClass('hidden').siblings().toggleClass('hidden');
        return false;
    };

    var saveEdition = function () {
        var parent = $(this).parents('div')[0];
        var sibling = $(parent).siblings();
        var elem_with_name = $(parent).find('[name]');
        $.each(elem_with_name, function(index, elem) {
            var name = $(elem).attr('name');
            var project_field = $('#' + name);
            var valor = $(elem).val();
            $(project_field).text(valor);
            if (valor.length == 0) {
                $(project_field).addClass('hidden');
            } else {
                $(project_field).removeClass('hidden');
            }
        });
        toggleSiblingDiv.bind(this)();
    };

    var startEdition = function () {
        var parent = $(this).parents('div')[0];
        var sibling = $(parent).siblings();
        var elem_with_id = $(parent).find('[id]');
        $.each(elem_with_id, function(index, elem) {
            var e = $(sibling).find('[name="' + elem.id + '"]');
            $(e).val($(elem).text());
            $(e).text($(elem).text());
        })
        toggleSiblingDiv.bind(this)();
    };

    $(function() {
        $('.edit.pattern').on('click', startEdition);
        $('.cancel.pattern').on('click', toggleSiblingDiv);
        $('.save.pattern').on('click', saveEdition);
        return false;
    });

})(jQuery);
