function changedCursor(e) {
    var editor = ace.edit("editor");
    position = editor.getCursorPosition();
    total_lines = editor.session.getLength();
    $('#line_position').html(position.row + 1);
    $('#column_position').html(position.column + 1);
    // $('#file_status').html(total_lines);
};


function init_asides() {
    $('article.editor aside nav a').unbind('click').bind('click', function(e) {
        e.preventDefault();
        var section = $($(this).attr('href'));
        $(this).toggleClass('active').siblings().removeClass('active');
        if ($(this).hasClass('active')) {
            section.parent().removeClass('active');
            $('section.editor').addClass(section.parent().attr('class'));
            section.parent().addClass('active');
            section.addClass('active').siblings().removeClass('active');
        } else {
            section.parent().removeClass('active').children().removeClass('active');
            $('section.editor').removeClass(section.parent().attr('class'));
        }
        return false;
    })
}


function process_lint_results(lint_results) {
    if (lint_results.length == 0) {
        return;
    }
    var editor = ace.edit('editor');
    var session = editor.getSession();
    var annotations = [];
    $('aside.results nav').append('<a href="#lint">lint</a>');
    $('aside.output_panel').append('<section id="lint">\
    <table>\
        <thead>\
            <tr><th>Pos</th><th>Message</th><th>Level</th></tr>\
        </thead>\
        <tbody></tbody>\
    </table></section>');
    var lint_table = $("section#lint table > tbody");

    // TODO: improve gutter icons
    var getLevelType = function(level) {
        level = level.toLowerCase();
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
        lint_table.append($tr);
        annotations[i] = {
            row: result.line - 1,  // gotoLine starts at 1, but annotations at 0 ?!?
            text: result.code + ': ' + result.message,
            type: getLevelType(result.level)
        };
    });
    session.setAnnotations(annotations);
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
    init_asides();
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
    language = $(option).val();
    mode = $(option).data('ace-mode') || language;
    editor.getSession().setMode('ace/mode/' + mode);
    $("#editor").data('language', language);
    $('#a-language').html(language);
}


function run(editor) {
    $('textarea[name="output"]').text('');
    $('textarea[name="metrics"]').text('');
    $("aside.output_panel").html('');
    $('aside.results nav').html('');
    $('section.editor').removeClass('output_panel');
    editor.getSession().clearAnnotations();
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


$(function() {
    var editor = ace.edit("editor");
    editor.getSession().setMode($("#editor").data('ace-mode'));
    editor.setTheme($("#editor").data('ace-theme'));
    editor.getSession().selection.on('changeCursor', changedCursor);
    changedCursor();
    $('button[name=run]').bind('click', function() { return run(editor) });
    $('select[name="languages"]').bind('change', function() {
        changeLanguage(editor);
    });
    $("button[name='increase_font']").bind('click', function() {
        increaseFontSize(editor, 1);
    })
    $("button[name='decrease_font']").bind('click', function() {
        increaseFontSize(editor, -1);
    })
    init_asides();
    increaseFontSize(editor, 0);
    editor.focus();
});
