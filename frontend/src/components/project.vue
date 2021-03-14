<template lang="pug">
section.project(:class='{expanded: expanded}')
    button.expand(@click='expanded = !expanded')
        svg.icon(:class='{ rotated: expanded }' fill='currentColor' viewBox='0 0 20 20')
            path(
                clip-rule='evenodd'
                d='M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z'
                fill-rule='evenodd'
            )
    .core
        .flex-justify
            h1.clickable(@click='expanded = !expanded') {{ title || i18n.$t("no_title") }}
            button.btn.btn-slim.btn-primary(v-if='expanded' @click='router.push(`/dojo/${id}`)') {{ i18n.$t("edit") }}
        .info
            span(:key='language' v-for='language in languages') {{ language }}
            span.tooltip(:data-text='timestamp') {{ i18n.relative_time(timestamp) }}
        auto-textarea.description(
            :modelValue='description'
            :read-only='true'
            v-if='expanded && description'
        )
        .details(v-show='expanded')
            .code
                nav.tab
                    button.active {{ i18n.$t("sourcecode") }}
                .tab_content
                    codemirror(:modelValue='code' :options='editor_options' ref='editor')
            .response
                nav.tab
                    button(
                        :class='{ active: current_tab === tab }'
                        :key='index'
                        @click='current_tab = tab'
                        v-for='(tab, index) in Object.keys(tabs)'
                    ) {{ tab }}
                .tab_content
                    auto-textarea(
                        :modelValue='stdin'
                        :read-only='true'
                        max-height='400px'
                        v-if='current_tab === "stdin"'
                    )
                    auto-textarea(
                        :modelValue='stdout'
                        :read-only='true'
                        max-height='400px'
                        v-if='current_tab === "stdout"'
                    )
                    auto-textarea(
                        :modelValue='stderr'
                        :read-only='true'
                        max-height='400px'
                        v-if='current_tab === "stderr"'
                    )
</template>

<script>
import { computed, ref, watch } from 'vue'

import { filepath_to_language } from '@/utils'
import { useRouter } from 'vue-router'
import { useI18n } from '@/plugins/i18n_plugin'
import codemirror from '@/components/codemirror'
import AutoTextarea from '@/components/AutoTextarea'

export default {
    name: 'project',
    components: {
        codemirror,
        AutoTextarea,
    },
    props: {
        id: String,
        title: {
            type: String,
            default: '',
        },
        description: {
            type: String,
            default: '',
        },
        timestamp: {
            type: Date,
            required: true,
        },
        sources: {
            type: Object,
            required: true,
        },
        commands: {
            type: Array,
            required: true,
        },
        responses: {
            type: Array,
            required: true,
        },
    },
    setup(props) {
        const code = computed(() => Object.values(props.sources)[0])
        const stdin = computed(() => props.commands[0].stdin)
        const stdout = computed(() => props.responses[0].stdout)
        const stderr = computed(() => props.responses[0].stderr)
        const languages = computed(() => {
            let result = []
            for (const filepath in props.sources) {
                result.push(filepath_to_language(filepath))
            }
            return result
        })

        const expanded = ref(false)
        const i18n = useI18n()
        const tabs = computed(() => {
            let result = {
                stdin: stdin.value,
                stdout: stdout.value,
                stderr: stderr.value,
            }
            Object.keys(result).forEach((k) => !result[k] && delete result[k])
            return result
        })

        const current_tab = ref(stderr.value ? 'stderr' : 'stdout')
        const editor = ref(null)
        const editor_options = {
            mode: languages.value[0].toLowerCase(),
            readOnly: true,
        }

        watch(expanded, (expanded) => {
            if (expanded) {
                // see https://stackoverflow.com/a/19970695/266362
                setTimeout(() => editor.value.editor.refresh(), 1)
            }
        })

        const router = useRouter()

        return {
            code,
            current_tab,
            editor,
            editor_options,
            expanded,
            i18n,
            languages,
            router,
            stdin,
            stdout,
            stderr,
            tabs,
        }
    },
}
</script>
