$(function() {
    $('a#submit').bind('click',
        function() {
            $('textarea[name="output"]').text('');
            $('textarea[name="errors"]').text('');
            $.getJSON($SCRIPT_ROOT + '/_do_the_thing',
                {
                language: $('select[name="language"]').val(),
                code: $('juicy-ace-editor').prop('editor').getValue(),
                input: $('textarea[name="input"]').val()
                },
                function(evaluation) {
                    $('textarea[name="output"]').text(evaluation.stdout);
                    $('textarea[name="errors"]').text(evaluation.stderr);
                }
            );
            return false;
        }
    );
    $('select[name="language"]').bind('change',
        function() {
            $('juicy-ace-editor').attr('mode', 'ace/mode/' + $(this).val());
        }
    );
});