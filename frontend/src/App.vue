<template lang="pug">
Header
router-view
Footer
</template>

<script>
import Header from './components/Header'
import Footer from './components/Footer'
import { messages } from './locales/messages'
import { provideI18n } from './plugins/i18n_plugin'

export default {
    name: 'Code Lab',
    components: {
        Header,
        Footer,
    },
    setup() {
        provideI18n({
            locale: Object.keys(messages).includes(navigator.language) ? navigator.language : 'en',
            messages: messages,
        })
    },
}
</script>
