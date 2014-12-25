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
                    $('textarea[name="output"]').text(evaluation.execution.stdout);
                    $('textarea[name="errors"]').text(evaluation.execution.stderr);
                }
            );
            return false;
        }
    );
    $('select[name="language"]').bind('change',
        function() {
            option = $(this).find('option:selected');
            mode = $(option).data('ace-mode') || $(option).attr('name');
            $('juicy-ace-editor').attr('mode', 'ace/mode/' + mode);
        }
    );
});