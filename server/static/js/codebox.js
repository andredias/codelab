function changedCursor(e) {
    var editor = ace.edit("editor");
    position = editor.getCursorPosition();
    total_lines = editor.session.getLength();
    $('#line_position').html(position.row + 1);
    $('#column_position').html(position.column + 1);
    // $('#file_status').html(total_lines);
};

function process_lint_results(lint_results) {
    var lint_table = $("#lint_results > tbody");
    var editor = ace.edit('editor');
    $.each(lint_results, function(i, result) {
        if (typeof result.column == 'undefined') {
            result.column = 1;
        }
        var $tr = $('<tr>').append(
            $('<td>').text(result.line),
            $('<td>').text(result.column),
            $('<td>').text(result.code),
            $('<td>').text(result.message),
            $('<td>').text(result.level)
        );
        $tr.bind('click', function() {
            editor.focus();
            // in ace, line starts at 1, but column at 0?!?
            editor.gotoLine(result.line, result.column - 1, true);
        });
        lint_table.append($tr);
    });
}


function process_output(evaluation) {
    process_lint_results(evaluation.lint);
    var output = '';
    if (evaluation.compilation) {
        output += evaluation.compilation.stdout + evaluation.compilation.stderr;
    }
    if (evaluation.execution) {
        output += evaluation.execution.stdout + evaluation.execution.stderr;
    }
    $('textarea[name="output"]').text(output);
}

function increaseFontSize(editor, value) {
    var currentFontSize = parseFloat($('#editor').css('font-size'), 10);
    currentFontSize += value;
    if (currentFontSize < 6) {
        return;
    }
    editor.setFontSize(currentFontSize);
}

function changeLanguage(editor) {
    option = $('select[name="languages"]').find('option:selected');
    mode = $(option).data('ace-mode') || $(option).val();
    editor.getSession().setMode('ace/mode/' + mode);
    $("#editor").data('language', $(option).val());
}

$(function() {
    var editor = ace.edit("editor");
    editor.getSession().setMode($("#editor").data('ace-mode'));
    editor.setTheme($("#editor").data('ace-theme'));
    editor.getSession().selection.on('changeCursor', changedCursor);
    changedCursor();
    $('button[name=run]').bind('click',
        function() {
            $('textarea[name="output"]').text('');
            $('textarea[name="metrics"]').text('');
            $("#lint_results > tbody").html('');
            $.getJSON($SCRIPT_ROOT + '/_do_the_thing',
                {
                language: $('#editor').data('language'),
                code: editor.getValue(),
                input: $('textarea[name="input"]').val()
                },
                process_output
            );
            return false;
        }
    );
    $('select[name="languages"]').bind('change', function() {
        changeLanguage(editor);
    });
    $("button[name='increase_font']").bind('click', function() {
        increaseFontSize(editor, 1);
    })
    $("button[name='decrease_font']").bind('click', function() {
        increaseFontSize(editor, -1);
    })
    increaseFontSize(editor, 0);
    editor.focus();
});