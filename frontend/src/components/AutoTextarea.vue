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
const style = ref({
    maxHeight: props.maxHeight,
})

onMounted(() => {
    set_style() // so textarea.value.value is set
})

function set_style() {
    style.value.height = 'auto'
    nextTick(() => {
        style.value.height = `${textarea.value.scrollHeight}px`
    })
}

watch(text, () => {
    set_style()
})
</script>

<style>
</style>
