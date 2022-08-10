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
        button.btn.btn-slim(
            @click="run_code",
            :disabled="controls_disabled",
            :class="{ 'btn-primary': !controls_disabled, 'btn-disabled': controls_disabled }"
        ) {{ i18n.$t('run_code') }}

        .botoes
            .link(
                @click="on_new_project",
                :data-tooltip="i18n.$t('new_project')",
                data-tooltip-location="left",
                :disabled="controls_disabled",
                :class="{ 'link-disabled': controls_disabled }"
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
                @click="copy_link",
                :data-tooltip="i18n.$t('copy_link')",
                data-tooltip-location="left",
                :disabled="controls_disabled",
                :class="{ 'link-disabled': controls_disabled }"
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
                        d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
                    )

            .link(
                @click="upload_file",
                :data-tooltip="i18n.$t('upload_file')",
                data-tooltip-location="left",
                :disabled="controls_disabled",
                :class="{ 'link-disabled': controls_disabled }"
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
        #new_project.dialog(v-if="show_new_project_dialog")
            h1 {{ i18n.$t('new_project') }}
            hr
            label(for="language")
                | {{ i18n.$t('language') }}:
            select(v-model="language", @change="on_language_changed")
                option(v-for="lang in languages")
                    | {{ lang }}

            label(for="based_on")
                | {{ i18n.$t('based_on') }}:
            select(v-model="example", @change="on_example_changed")
                option(:value="{}") {{ i18n.$t('blank_project') }}
                option(:value="e", v-for="e in examples_by_language")
                    | {{ e.title }}

            .actions
                button.btn.btn-slim.btn-cancel(
                    @click="close_new_project_dialog(false)"
                ) {{ i18n.$t('cancel') }}
                button.btn.btn-primary.btn-slim(
                    @click="close_new_project_dialog(true)"
                ) {{ i18n.$t('create') }}

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
import { inject, reactive, ref, computed, watch, onMounted, isProxy } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import codemirror from '../components/codemirror.vue'
import AutoTextarea from '../components/AutoTextarea.vue'
import { get_project, run_project, load_examples } from '../codelab.js'

const code = ref('')
const responses = reactive([])
const stdin = ref('')
const stdout = computed(() => responses.map(r => r.stdout).join(''))
const stderr = computed(() => responses.map(r => r.stderr).join(''))

const cursor_pos = ref({ line: 0, ch: 0 })
const theme = ref('dark')
const editor_options = ref({
    mode: 'Python',
    theme: 'blackboard',
})
const editor = ref(null)
const code_uploader = ref(null)

const show_new_project_dialog = ref(false)
const old_code = ref('')
const old_responses = reactive([])
const old_stdin = ref('')
const old_language = ref('')
const old_history = ref('')

const i18n = inject('i18n')
const is_light_theme = computed(() => theme.value === 'light')
const _language = ref('')
const language = computed({
    get() {
        return _language.value
    },
    set(value) {
        _language.value = value
        editor_options.value.mode = value.toLowerCase()
    },
})
const languages = reactive([])
const examples = reactive([])
const example = ref({})

const examples_by_language = computed(() => examples.filter(e => e.language.toLowerCase() === language.value.toLowerCase()
))

const controls_disabled = computed(() => show_new_project_dialog.value)


onMounted(async () => {
    await load_examples()
    Object.assign(examples, JSON.parse(localStorage.getItem('examples')))
    languages.push(...JSON.parse(localStorage.getItem('languages')))
})


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
    if (controls_disabled.value) {
        return
    }
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
        responses.length = 0
        if (params.id) {
            let project = await get_project(params.id)
            editor.value.editor.setValue(project.sourcecode)
            responses.push(...project.responses)
            stdin.value = project.stdin || ''
            language.value = project.language
        } else {
            stdin.value = ''
            language.value = 'Python'
        }
    },
    { immediate: true }  // see: https://stackoverflow.com/a/71354391
)

async function run_code() {

    let project = await run_project(editor_options.value.mode, code.value, stdin.value)
    responses.length = 0
    responses.push(...project.responses)

    history.pushState({}, null, `/dojo/${project.id}`)
}

function on_new_project() {
    if (controls_disabled.value) {
        return
    }
    show_new_project_dialog.value = true
    old_code.value = code.value
    old_stdin.value = stdin.value
    old_responses.length = 0
    old_responses.push(...responses)
    old_history.value = history.state.current
    old_language.value = language.value
    on_language_changed()
}

function close_new_project_dialog(create_project) {
    show_new_project_dialog.value = false
    if (!create_project) {
        editor.value.editor.setValue(old_code.value)
        stdin.value = old_stdin.value
        responses.length = 0
        responses.push(...old_responses)
        language.value = old_language.value
        history.pushState({}, null, old_history.value)
    }
}

function on_language_changed() {
    example.value = {}
    on_example_changed()
}

function on_example_changed() {
    if (example.value.id === undefined) {
        history.pushState({}, null, '/')
        stdin.value = ''
        responses.length = 0
        editor.value.editor.setValue('')
    } else {
        history.pushState({}, null, `/dojo/${example.value.id}`)
        stdin.value = example.value.stdin
        responses.length = 0
        responses.push(...example.value.responses)
        editor.value.editor.setValue(example.value.sourcecode)
    }
}

function copy_link() {
    if (controls_disabled.value) {
        return
    }
    let link = window.location.href
    navigator.clipboard.writeText(link)
    alert(i18n.$t('link_copied') + ':\n' + link)
}
</script>

<style scoped lang="stylus">

border_color = #c7c7c7

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

input
select
    display block

select
option
    text-transform capitalize

.actions
    display flex
    justify-content flex-start
    gap 1rem
    margin 1rem 0

input
select
    color black
    background white
    line-height 1.5
    border 1px solid border_color
    padding 0.4rem
    color text_color
    display block

.link-disabled
    opacity 0.5
</style>
