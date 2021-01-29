<template lang="pug">
Header
router-view
Footer
</template>

<script>
// import { onMounted } from "vue";
import Header from "./components/Header";
import Footer from "./components/Footer";
import { messages } from "./locales/messages";
import { provideI18n } from "./plugins/i18n_plugin";

export default {
    name: "Code Lab",
    components: {
        Header,
        Footer,
    },
    setup() {
        // onMounted( () => {
        //     provideI18n({
        //         locale: navigator.language,
        //         messages: messages,
        //     })
        // })
        provideI18n({
            locale: 'pt-BR',
            messages: messages,
        });
    },
};
</script>
