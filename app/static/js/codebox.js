'use strict';

function changedCursor(e) {
    var editor = ace.edit("editor");
    var position = editor.getCursorPosition();
    var total_lines = editor.session.getLength();
    $('#line_position').html(position.row + 1);
    $('#column_position').html(position.column + 1);
    // $('#file_status').html(total_lines);
};


function process_lint_results(editor, evaluation) {
    var lint_results = evaluation.lint;
    if (lint_results.length == 0) {
        return null;
    }
    var session = editor.getSession();
    var annotations = [];
    var tbody = $("<tbody />");

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
    $.each(lint_results, function(i, result) {
        if (typeof result.column == 'undefined') {
            result.column = 1;
        }
        var $tr = $('<tr>').append(
            $('<td>').text(result.line + ':' + result.column),
            // $('<td>').text(result.code),
            $('<td>').text(result.message),
            $('<td>').text(result.level)
        );
        $tr.bind('click', function() {
            editor.focus();
            // in ace, line starts at 1, but column at 0?!?
            editor.gotoLine(result.line, result.column - 1, true);
        });
        tbody.append($tr);
        annotations[i] = {
            row: result.line - 1,  // gotoLine starts at 1, but annotations at 0 ?!?
            text: result.code + ': ' + result.message,
            type: getLevelType(result.level)
        };
    });
    session.setAnnotations(annotations);
    var lint_table = $('<table>\
        <thead>\
            <tr><th>Position</th><th>Message</th><th>Level</th></tr>\
        </thead>\
    </table>').append(tbody);
    return lint_table;
}


function process_output(evaluation) {
    var output = '';
    if (evaluation.compilation) {
        output += evaluation.compilation.stdout + evaluation.compilation.stderr;
    }
    if (evaluation.execution) {
        output += evaluation.execution.stdout + evaluation.execution.stderr;
    }
    return $('<textarea rows="10" readonly="readonly" />').text(output)
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
        terminals.clear();
        editor.getSession().clearAnnotations();
        $.getJSON($SCRIPT_ROOT + '/_do_the_thing',
            {
            language: ddl.getValue(),
            code: ddl.editor.getValue(),
            input: $('#input_data').val()
            },
            function(evaluation) {
                $('#spinner').removeClass('active');
                var lint_results = process_lint_results(editor, evaluation);
                if (lint_results) {
                    terminals.addTab('Lint', lint_results);
                }
                terminals.addTab('Output', process_output(evaluation)).click();
            }
        );
        return false;
    });
    increaseFontSize(editor, 0);
    editor.focus();
});
