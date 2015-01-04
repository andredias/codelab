$(function() {
    var editor = ace.edit("editor");
    editor.getSession().setMode(EditorParams.mode);
    editor.setTheme(EditorParams.theme);
    $('a#submit').bind('click',
        function() {
            $('textarea[name="output"]').text('');
            $('textarea[name="errors"]').text('');
            $.getJSON($SCRIPT_ROOT + '/_do_the_thing',
                {
                language: language,
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