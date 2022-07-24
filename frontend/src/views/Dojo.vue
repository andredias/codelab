<template lang="pug">
.dojo.miolo
    //- .header-container
    //-     header
    //-         div
    //-             h3.bread-crumbs
    //-                 router-link(to='/') {{ i18n.$t("home") }}
    //-                 router-link(to='/languages/python') Python
    //-                 span {{ title }}
    .menu
        button.btn.btn-primary.btn-slim(@click="run_code") {{ i18n.$t('run_code') }}

    .editor
        .box
            codemirror(
                :options="editor_options",
                @cursor_moved="update_cursor",
                ref="editor",
                v-model="code"
            )
            .cursor(:class="{ light: is_light_theme }")
                div
                    span {{ i18n.$t('theme') }}:
                    a(
                        :class="{ selected: is_light_theme }",
                        @click.prevent="change_theme('light')",
                        href="#"
                    ) {{ i18n.$t('light') }}
                    a(
                        :class="{ selected: !is_light_theme }",
                        @click.prevent="change_theme('dark')",
                        href="#"
                    ) {{ i18n.$t('dark') }}
                div
                    span.programming_language {{ editor_options.mode }}
                div
                    span {{ i18n.$t('line') }}:
                    span.cursor_pos {{ cursor_pos.line + 1 }}
                    span {{ i18n.$t('column') }}:
                    span.cursor_pos {{ cursor_pos.ch + 1 }}
    //- .lint
    //-     h2 Lint
    .input-output
        .upload-run
            .link(@click="upload_file")
                svg.icon(
                    fill="none",
                    stroke="currentColor",
                    viewBox="0 0 24 24"
                )
                    path(
                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12",
                        stroke-linecap="round",
                        stroke-linejoin="round",
                        stroke-width="2"
                    )
                span &nbsp; {{ i18n.$t('upload_code_from_file') }}
                input#code_uploader(
                    @change="on_file_picked",
                    name="code_uploader",
                    ref="code_uploader",
                    style="display: none",
                    type="file"
                )
        .input
            h2 stdin
            auto-textarea.code(v-model="stdin")

        .output(v-show="stdout")
            h2 stdout
            auto-textarea.code(
                :read-only="true",
                max-height="90vh",
                v-model="stdout"
            )

        .output(v-show="stderr")
            h2 stderr
            auto-textarea.code(
                :read-only="true",
                max-height="90vh",
                v-model="stderr"
            )
</template>

<script setup>
import { inject, ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import codemirror from '../components/codemirror.vue'
import AutoTextarea from '../components/AutoTextarea.vue'
import { get_project, run_project } from '../codelab.js'

const code = ref('')
const stdin = ref('')
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

const i18n = inject('i18n')
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


const route = useRoute()

watch(
    () => route.params,
    async (params) => {
        if (params.id) {
            let project = await get_project(params.id)
            editor.value.editor.setValue(project.sourcecode)
            let response = project.responses[0]
            stdout.value = response.stdout || ''
            stderr.value = response.stderr || ''
            stdin.value = project.stdin || ''
            editor_options.value.mode = project.language.toLowerCase()
        } else {
            stdout.value = ''
            stdin.value = ''
            stderr.value = ''
            editor_options.value.mode = 'python'
        }
    },
    { immediate: true }  // see: https://stackoverflow.com/a/71354391
)

async function run_code() {
    stdout.value = ''
    stderr.value = ''
    exit_code.value = 0
    let project = await run_project(editor_options.value.mode, code.value, stdin.value)
    let response = project.responses[0]
    stdout.value = response.stdout
    stderr.value = response.stderr
    exit_code.value = response.exit_code
    history.pushState({}, null, `/dojo/${project.id}`)
}

</script>
