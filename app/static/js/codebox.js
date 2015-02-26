'use strict';

function changedCursor(e) {
    var editor = ace.edit("editor");
    var position = editor.getCursorPosition();
    var total_lines = editor.session.getLength();
    $('#line_position').html(position.row + 1);
    $('#column_position').html(position.column + 1);
    // $('#file_status').html(total_lines);
};


function process_lint_data(editor, lint_data) {
    if (lint_data.length == 0) {
        return null;
    }
    $.each($('#lint_table tbody tr'), function(i, elem) {
        var coord = $(elem).first().text().split(':');
        coord = [parseInt(coord[0]), parseInt(coord[1])];
        $(elem).bind('click', function() {
            editor.focus();
            // in ace, line starts at 1, but column at 0?!?
            editor.gotoLine(coord[0], coord[1] - 1, true);
        });
    });

    // TODO: improve gutter icons
    var getLevelType = function(level) {
        var level = level.toLowerCase();
        var levelmap = {
            'fatal': 'error',
            'convention': 'info',
            'refactor': 'info'
        };
        return levelmap[level] || level;
    }
    var annotations = [];
    $.each(lint_data, function(i, result) {
        annotations[i] = {
            row: result.line - 1,  // gotoLine starts at 1, but annotations at 0 ?!?
            text: result.code + ': ' + result.message,
            type: getLevelType(result.level)
        };
    });
    editor.getSession().setAnnotations(annotations);
}


function increaseFontSize(editor, value) {
    var currentFontSize = parseFloat($('#editor').css('font-size'), 10);
    currentFontSize += value;
    if (currentFontSize < 6) {
        return;
    }
    editor.setFontSize(currentFontSize);
}


$(function() {
    var editor = ace.edit("editor");
    editor.setTheme($("#editor").data('ace-theme'));
    editor.getSession().selection.on('changeCursor', changedCursor);
    changedCursor();
    $("#increase_font").on('click', function() {
        increaseFontSize(editor, 1);
        return false;
    })
    $("#decrease_font").on('click', function() {
        increaseFontSize(editor, -1);
        return false;
    })
    var terminals = new Terminals($('dl.terminals'));
    var ddl = new DropDownLanguage(editor, $('#a-language'));
    var config = new DropDown(editor, $('#config'));
    $(document).on('click', function() {
        // disable all dropdowns
        $('.menu').removeClass('active');
    });

    $('button[name=run]').on('click', function() {
        $('#spinner').addClass('active');
        var title = $('<input />').attr('type', 'text').attr('name', 'title')
                                .val($('#project_title').text());
        var description = $('<textarea />').attr('name', 'description')
                                           .val($('#project_description').text());
        var input = $('<textarea />').attr('name', 'input').val($('#input_data').val());
        var source = $('<textarea />').attr('name', 'source').val(ddl.editor.getValue());
        var language = $('<input />').attr('type', 'text').attr('name', 'language')
                                     .val(ddl.getValue());
        $('#run_code').append(title).append(description)
                      .append(input).append(source).append(language).submit();
    });
    increaseFontSize(editor, 0);
    editor.focus();
    process_lint_data(editor, lint_data);
});
