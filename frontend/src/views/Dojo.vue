<template lang="pug">
.dojo
    .header-container
        header
            div
                h3.bread-crumbs
                    router-link(to='/') Home
                    router-link(to='/languages/python') Python
                    span {{ title }}
    main
        .projeto
            .titulo(v-if='!editing_description')
                h1 {{ title || i18n.$t("no_title") }}
                svg.icon.link(
                    fill='none',
                    viewBox='0 0 24 24',
                    stroke='currentColor',
                    @click='start_editing_title'
                )
                    path(
                        stroke-linecap='round',
                        stroke-linejoin='round',
                        stroke-width='2',
                        d='M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z'
                    )
            .descricao.box(v-if='!editing_description && description')
                p {{ description }}

            .edit_project_description(v-if='editing_description')
                label(for='project_title') {{ i18n.$t("title") }}
                input#project_title(type='text', v-model='temp_title')
                label(for='project_description') {{ i18n.$t("description") }}
                textarea#project_description(v-model='temp_description')
                div
                    button.btn.btn-primary(@click='confirm_title_alteration') {{ i18n.$t("change") }}
                    button.btn.btn-secondary(@click='editing_description = false') {{ i18n.$t("cancel") }}

        //- .stats
        //-     h2 {{ i18n.$t("statistics") }}

        .editor
            h2 Editor
            .box
                codemirror(
                    v-model='code',
                    :options='editor_options',
                    @cursor_moved='update_cursor',
                    ref='editor'
                )
                .cursor(:class='{ light: is_light_theme }')
                    div
                        span {{ i18n.$t("theme") }}:
                        a(
                            href='#',
                            :class='{ selected: is_light_theme }',
                            @click.prevent='change_theme("light")'
                        ) {{ i18n.$t("light") }}
                        a(
                            href='#',
                            :class='{ selected: !is_light_theme }',
                            @click.prevent='change_theme("dark")'
                        ) {{ i18n.$t("dark") }}
                    div
                        span Python
                    div
                        span {{ i18n.$t("line") }}:
                        span.cursor_pos {{ cursor_pos.line + 1 }}
                        span {{ i18n.$t("column") }}:
                        span.cursor_pos {{ cursor_pos.ch + 1 }}
        //- .lint
        //-     h2 Lint
        .input-output
            .upload-run
                button.btn.btn-primary(@click='run_code') {{ i18n.$t("run_code") }}
                .link(@click='upload_file')
                    svg.icon(fill='none', viewBox='0 0 24 24', stroke='currentColor')
                        path(
                            stroke-linecap='round',
                            stroke-linejoin='round',
                            stroke-width='2',
                            d='M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12'
                        )
                    span &nbsp; {{ i18n.$t("upload_code_from_file") }}
                    input#code_uploader(
                        type='file',
                        name='code_uploader',
                        style='display: none',
                        ref='code_uploader',
                        @change='on_file_picked'
                    )
            .input
                input#custom_input(type='checkbox', v-model='checked_input')
                label(for='custom_input') {{ i18n.$t("define_input_data") }}
                div(v-show='checked_input')
                    h2 stdin
                    textarea.code(v-model='input')

            .output(v-show='stdout')
                h2 stdout
                textarea.code(readonly, v-model='stdout')
            .output(v-show='stderr')
                h2 stderr
                textarea.code(readonly, v-model='stderr')
</template>

<script>
import codemirror from '@/components/codemirror'
import { ref, computed } from 'vue'
import { useI18n } from '@/plugins/i18n_plugin'
import axios from 'axios'

export default {
    components: {
        codemirror,
    },
    setup() {
        const code = ref('')
        const lint = ref({})
        const input = ref('')
        const checked_input = ref(false)
        const stdout = ref('')
        const stderr = ref('')
        const exit_code = ref(0)
        const cursor_pos = ref({ line: 0, ch: 0 })
        const theme = ref('dark')
        const editor_options = ref({
            mode: 'python',
            theme: 'blackboard',
        })
        const editor = ref(null)
        const code_uploader = ref(null)
        const project_id = ref(null)

        const title = ref('')
        const description = ref('')
        const temp_title = ref('')
        const temp_description = ref('')
        const editing_description = ref(false)

        const i18n = useI18n()
        const is_light_theme = computed(() => theme.value === 'light')

        function change_theme(style) {
            theme.value = style
            if (theme.value === 'light') {
                editor_options.value.theme = 'github'
            } else {
                editor_options.value.theme = 'blackboard'
            }
        }

        function update_cursor(position) {
            cursor_pos.value = position
        }

        function set_cursor_position(line, ch) {
            editor.value.editor.setCursor(line - 1, ch - 1)
            editor.value.editor.focus()
        }

        function upload_file() {
            code_uploader.value.click()
        }

        function on_file_picked(event) {
            const files = event.target.files
            const fileReader = new FileReader()
            fileReader.addEventListener('load', () => {
                editor.value.editor.setValue(fileReader.result)
                editor.value.editor.focus()
            })
            fileReader.readAsText(files[0])
        }

        function start_editing_title() {
            editing_description.value = true
            temp_title.value = title.value
            temp_description.value = description.value
        }

        async function confirm_title_alteration() {
            title.value = temp_title.value
            description.value = temp_description.value
            editing_description.value = false
        }

        async function run_code() {
            stdout.value = ''
            stderr.value = ''
            exit_code.value = 0
            let resp = await axios.post(`${process.env.VUE_APP_API_URL}/projects`, {
                sources: { 'main.py': code.value },
                commands: [{ type: 'python', command: 'python main.py', timeout: 0.1 }],
                title: title.value,
                description: description.value,
            })
            let data = resp.data
            project_id.value = data['id']
            let responses = data['responses']
            if (responses.length > 0) {
                stdout.value = responses[0]['stdout']
                stderr.value = responses[0]['stderr']
                exit_code.value = responses[0]['exit_code']
            }
            console.log(resp)
        }

        return {
            run_code,
            code,
            lint,
            checked_input,
            input,
            stdout,
            stderr,
            exit_code,
            cursor_pos,
            theme,
            change_theme,
            is_light_theme,
            editor_options,
            update_cursor,
            set_cursor_position,
            editor,
            upload_file,
            code_uploader,
            on_file_picked,
            title,
            description,
            temp_title,
            temp_description,
            editing_description,
            start_editing_title,
            confirm_title_alteration,
            i18n,
        }
    },
}
</script>
