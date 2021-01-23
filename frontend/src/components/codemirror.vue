<template lang="pug">
textarea(ref="textarea")
</template>

<script>
import { ref, markRaw, onMounted } from 'vue'
import CodeMirror from 'codemirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/blackboard.css'
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
    emits: ["update:modelValue"],
    setup(props, { emit }) {
        const textarea = ref(null)
        const codemirror = ref(null)

        onMounted(() => {
            const defaultOptions = {
                lineNumbers: true,
                mode: 'python',
                theme: 'blackboard',
            }
            codemirror.value = markRaw(CodeMirror.fromTextArea(textarea.value, {...defaultOptions, ...props.options}))
            codemirror.value.setValue(props.modelValue)
            codemirror.value.on('change', cm => {
                emit('update:modelValue', cm.getValue())
            })
        })
        return { textarea }
    }

}
</script>
