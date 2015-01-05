$(function() {
    var editor = ace.edit("editor");
    editor.getSession().setMode($("#editor").data('ace-mode'));
    editor.setTheme($("#editor").data('ace-theme'));
    $('a#submit').bind('click',
        function() {
            $('textarea[name="output"]').text('');
            $('textarea[name="errors"]').text('');
            $.getJSON($SCRIPT_ROOT + '/_do_the_thing',
                {
                language: $('#editor').data('language'),
                code: editor.getValue(),
                input: $('textarea[name="input"]').val()
                },
                function(evaluation) {
                    $('textarea[name="output"]').text(evaluation.execution.stdout);
                    $('textarea[name="errors"]').text(evaluation.execution.stderr);
                }
            );
            return false;
        }
    );
});