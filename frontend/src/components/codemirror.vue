<template lang="pug">
textarea(ref="textarea")
</template>

<script>
import { ref, markRaw, onMounted, watch } from 'vue'
import CodeMirror from 'codemirror'
import 'codemirror/lib/codemirror.css'
import '@/assets/blackboard.css'
import '@/assets/github-theme.css'
import 'codemirror/mode/python/python'
import 'codemirror/mode/javascript/javascript'
import 'codemirror/mode/rust/rust'
import 'codemirror/mode/go/go'
import 'codemirror/mode/sql/sql'

export default {
    name: 'codemirror',
    props: {
        modelValue: String,
        options: {
            type: Object,
            default: () => ({})
        },
    },
    emits: ["update:modelValue", "cursor_moved"],
    setup(props, { emit }) {
        const textarea = ref(null)
        const editor = ref(null)


        onMounted(() => {
            const defaultOptions = {
                lineNumbers: true,
                mode: 'python',
                theme: 'blackboard',
                lineWrapping: true,
            }
            editor.value = markRaw(CodeMirror.fromTextArea(textarea.value, {...defaultOptions, ...props.options}))
            editor.value.setValue(props.modelValue)
            editor.value.on('change', cm => {
                emit('update:modelValue', cm.getValue())
            })
            editor.value.on('cursorActivity', cm => {
                emit('cursor_moved', cm.getCursor())
            })
        })


        watch(
            () => props.options,
            (options) => {
                for (const key in options) {
                    editor.value.setOption(key, options[key])
                }
            },
            { deep: true }
        )

        return { textarea, editor }
    }

}
</script>
