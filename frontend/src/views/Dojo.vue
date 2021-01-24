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
                codemirror(v-model="code" :options="editor_options")
                .cursor(:class="{ light: is_light_theme }")
                    div
                        span Tema:
                        a(href="#" :class="{ selected: is_light_theme }" @click.prevent="change_theme('light')") Light
                        a(href="#" :class="{ selected: !is_light_theme }" @click.prevent="change_theme('dark')") Dark
                    div
                        span Python
                    div
                        span Linha: 4
                        span Coluna: 10
        .lint
            h1 Lint
        .input-output
            div.upload-run
                button.btn.btn-primary Run Code
                a(href="#")
                    svg(class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor")
                        path(stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12")
                    span &nbsp; upload code from file
            div.input
                input(type="checkbox" name="custom_input" v-model="checked_input")
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
        const code = ref('teste 123')
        const lint = ref({})
        const input = ref('')
        const checked_input = ref(false)
        const output = ref('teste\n123')
        const cursor_pos = ref({})
        const theme = ref('dark')
        const editor_options = ref({
            mode: 'python',
            theme: 'blackboard',
        })

        const change_theme = (style) => {
            theme.value = style
            if (theme.value === 'light') {
                editor_options.value.theme = 'github'
            } else {
                editor_options.value.theme = 'blackboard'
            }
        }

        const is_light_theme = computed(() => theme.value === 'light')


        return { code, lint, checked_input, input, output, cursor_pos, theme, change_theme, is_light_theme, editor_options }
    }

}
</script>
