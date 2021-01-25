<template lang="pug">
.dojo
    .header-container
        header
            div
                h3.bread-crumbs
                    router-link(to="/") Home
                    router-link(to="/languages/python") Python
                    span Título do Projeto
    main
        .projeto
            .titulo
                h1 Título do Projeto
                svg(class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor")
                    path(stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z")
            .descricao.box
                p
                    | Deploy web apps of all kinds, from large scale enterprise APIs to static websites for individuals. Fill out the form to try a demo of our platform
        .stats
            h1 Estatísticas
        .editor
            h1 Editor
            .box
                codemirror(v-model="code" :options="editor_options" @cursor_moved="update_cursor" ref="editor")
                .cursor(:class="{ light: is_light_theme }")
                    div
                        span Tema:
                        a(href="#" :class="{ selected: is_light_theme }" @click.prevent="change_theme('light')") Light
                        a(href="#" :class="{ selected: !is_light_theme }" @click.prevent="change_theme('dark')") Dark
                    div
                        span Python
                    div
                        span Linha:
                        span.cursor_pos {{ cursor_pos.line + 1 }}
                        span Coluna:
                        span.cursor_pos {{ cursor_pos.ch + 1 }}
        .lint
            h1 Lint
        .input-output
            div.upload-run
                button.btn.btn-primary Run Code
                .link(@click="upload_file")
                    svg(class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor")
                        path(stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12")
                    span &nbsp; upload code from file
                    input(type="file" name="code_uploader" style="display:none" ref="code_uploader" id="code_uploader" @change="on_file_picked")
            div.input
                input(type="checkbox" id="custom_input" v-model="checked_input")
                label(for="custom_input") Definir dados de entrada
                textarea.code(v-show="checked_input" v-model="input")

            div.output(v-if="output")
                h1 Output
                textarea.code(readonly v-model="output")
</template>

<script>
import codemirror from '@/components/codemirror'
import { ref, computed } from 'vue'

export default {
    components: {
        codemirror,
    },
    setup() {
        const code = ref('')
        const lint = ref({})
        const input = ref('')
        const checked_input = ref(false)
        const output = ref('')
        const cursor_pos = ref({line: 0, ch: 0})
        const theme = ref('dark')
        const editor_options = ref({
            mode: 'python',
            theme: 'blackboard',
        })
        const editor = ref(null)
        const code_uploader = ref(null)

        const change_theme = (style) => {
            theme.value = style
            if (theme.value === 'light') {
                editor_options.value.theme = 'github'
            } else {
                editor_options.value.theme = 'blackboard'
            }
        }

        const update_cursor = (position) => {
            cursor_pos.value = position
        }

        const is_light_theme = computed(() => theme.value === 'light')

        const set_cursor_position = (line, ch) => {
            editor.value.editor.setCursor(line - 1, ch - 1)
            editor.value.editor.focus()
        }

        const upload_file = () => {
            code_uploader.value.click()
        }

        const on_file_picked = (event) => {
            const files = event.target.files
            const fileReader = new FileReader()
            fileReader.addEventListener('load', () => {
                code.value = fileReader.result
                editor.value.editor.focus()
            })
            fileReader.readAsText(files[0])
        }


        return { code, lint, checked_input, input, output, cursor_pos, theme, change_theme, is_light_theme, editor_options, update_cursor, set_cursor_position, editor, upload_file, code_uploader, on_file_picked }
    }

}
</script>
