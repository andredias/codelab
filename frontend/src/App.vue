<script setup>
import { provide } from 'vue'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { messages } from './locale_messages'
import { createI18n } from './plugins/i18n'


document.title = "Code Lab"
provide('i18n', createI18n({
    locale: Object.keys(messages).includes(navigator.language)
        ? navigator.language
        : "en",
    messages: messages,
}))

</script>

<template lang="pug">
Header
router-view
Footer
</template>
