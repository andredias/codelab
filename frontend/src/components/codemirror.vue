<template lang="pug">
textarea(ref="textarea")
</template>

<script setup>
import { ref, markRaw, onMounted, watch } from 'vue'
import CodeMirror from 'codemirror'
import 'codemirror/lib/codemirror.css'
import '/src/assets/blackboard.css'
import '/src/assets/github-theme.css'
import 'codemirror/mode/python/python'
import 'codemirror/mode/javascript/javascript'
import 'codemirror/mode/rust/rust'
import 'codemirror/mode/go/go'
import 'codemirror/mode/sql/sql'


const props = defineProps({
    modelValue: {
        type: String,
        default: '',
    },
    options: {
        type: Object,
        default: () => ({}),
    },
})
const emit = defineEmits(['update:modelValue', 'cursor_moved'])
const textarea = ref(null)
const editor = ref(null)

defineExpose({
    editor,
})

onMounted(() => {
    const defaultOptions = {
        lineNumbers: true,
        mode: 'python',
        theme: 'blackboard',
        lineWrapping: true,
        indentUnit: 4,
    }
    editor.value = markRaw(
        CodeMirror.fromTextArea(textarea.value, {
            ...defaultOptions,
            ...props.options,
        })
    )
    editor.value.setValue(props.modelValue)
    editor.value.on('change', (cm) => {
        emit('update:modelValue', cm.getValue())
    })
    editor.value.on('cursorActivity', (cm) => {
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
</script>
