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

        .botoes
            .link(
                @click="",
                :data-tooltip="i18n.$t('new_project')",
                data-tooltip-location="left"
            )
                svg.icon(
                    xmlns="http://www.w3.org/2000/svg",
                    fill="none",
                    viewbox="0 0 24 24",
                    stroke="currentColor",
                    stroke-width="2"
                )
                    path(
                        stroke-linecap="round",
                        stroke-linejoin="round",
                        d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                    )

            .link(
                @click="",
                :data-tooltip="i18n.$t('share_project')",
                data-tooltip-location="left"
            )
                svg.icon(
                    xmlns="http://www.w3.org/2000/svg",
                    fill="none",
                    viewbox="0 0 24 24",
                    stroke="currentColor",
                    stroke-width="2"
                )
                    path(
                        stroke-linecap="round",
                        stroke-linejoin="round",
                        d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"
                    )

            .link(
                @click="upload_file",
                :data-tooltip="i18n.$t('upload_file')",
                data-tooltip-location="left"
            )
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
                input#code_uploader(
                    @change="on_file_picked",
                    name="code_uploader",
                    ref="code_uploader",
                    style="display: none",
                    type="file"
                )

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

<style scoped lang="stylus">

.dojo
    background-color background_color


    margin 0 auto
    padding 1rem 0
    width 90vw
    display flex
    flex-flow column
    gap 0.75rem


    h1
    h2
        color cor_titulo
        font-size 1.2rem
        font-weight 600
        margin 1rem 0 0.5rem

    h2
        font-size 1rem


    .menu
        position relative

        .titulo
            display flex
            justify-content space-between
            align-items center

    .editor
        padding 0

        .cursor
            background white
            monospace()
            font-size 0.9rem
            color cor_texto
            display flex
            justify-content space-between
            padding 0.25rem 1rem

            &.light
                background #efefef

            a.selected
                border-bottom 1px solid

            div
                * + *
                    margin-left 1rem

            span.cursor_pos
                min-width 3ch
                display inline-block
                text-align right
                margin-left 0

            span.programming_language
                text-transform capitalize

    .input-output

        margin 0

        label
            padding-left 0.5rem

        textarea.code
            display block
            margin-top 0.5rem
            resize none
            min-height 10ch
            width 100%
            font-size 0.9rem
            line-height 1.25rem
            monospace()

        .upload-run
            display flex
            justify-content end

        .input
            margin-top 1rem

.menu
    display flex
    justify-content space-between
    align-items flex-end

.botoes
    display flex
    gap 1rem
    justify-content space-between

.code
    font-family monospace
</style>
