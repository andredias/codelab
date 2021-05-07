<template lang="pug">
section.project(:class='{ expanded: expanded }')
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
            button.btn.btn-slim.btn-primary(@click='router.push(`/dojo/${id}`)' v-if='expanded') {{ i18n.$t("edit") }}
        .info
            span {{ language }}
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
                    codemirror(:modelValue='sourcecode' :options='editor_options' ref='editor')
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
        sourcecode: {
            type: String,
            required: true,
        },
        language: {
            type: String,
            required: true,
        },
        stdin: {
            type: String,
            default: '',
        },
        stdout: {
            type: String,
            default: '',
        },
        stderr: {
            type: String,
            default: '',
        },
        exit_code: {
            type: Number,
            default: 0,
        },
    },
    setup(props) {
        const expanded = ref(false)
        const i18n = useI18n()
        const tabs = computed(() => {
            let result = {
                stdin: props.stdin,
                stdout: props.stdout,
                stderr: props.stderr,
            }
            Object.keys(result).forEach((k) => !result[k] && delete result[k])
            return result
        })

        const current_tab = ref(props.stderr ? 'stderr' : 'stdout')
        const editor = ref(null)
        const editor_options = {
            mode: props.language.toLowerCase(),
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
            current_tab,
            editor,
            editor_options,
            expanded,
            i18n,
            router,
            tabs,
        }
    },
}
</script>
