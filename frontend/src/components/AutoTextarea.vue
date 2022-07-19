<template lang="pug">
textarea(:readonly="readOnly", :style="style", ref="textarea", v-model="text")
</template>

<script setup>
import { computed, nextTick, ref, watch, onMounted } from 'vue'


const props = defineProps({
    modelValue: {
        type: String,
        default: '',
    },
    readOnly: {
        type: Boolean,
        default: false,
    },
    maxHeight: {
        type: String,
        default: '',
    },
})
const emit = defineEmits(['update:modelValue'])
const text = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value),
})
const textarea = ref(null)
const number_of_lines = computed(() => (text.value.match(/\n/g) || []).length + 1)
const style = ref({
    maxHeight: props.maxHeight,
})

onMounted(() => {
    nextTick(set_style) // so textarea.value.value is set
})

function parse_value(value) {
    return parseInt(value) || 0
}

function set_style() {
    let height = 'auto'
    if (text.value) {
        let v = window.getComputedStyle(textarea.value)
        let calculated_height = (
            number_of_lines.value * parse_value(v.lineHeight) +
            parse_value(v.paddingTop) +
            parse_value(v.paddingBottom) +
            parse_value(v.borderWidth)
        )
        height = Math.max(parse_value(v.minHeight), calculated_height)
    }
    style.value.height = height + 'px'
}

watch(number_of_lines, () => {
    set_style()
})
</script>

<style>
</style>
