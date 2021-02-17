<template lang="pug">
header.main
    section
        h1.logotipo
            router-link(to='/') Code Lab
        nav
            router-link(to='/') {{ i18n.$t("home") }}
            router-link(to='/dojo') Dojo
            router-link(to='/how') {{ i18n.$t("how_it_works") }}
            span(@click='toogle_lang', style='cursor: pointer')
                svg.icon(fill='none', viewBox='0 0 24 24', stroke='currentColor')
                    path(
                        stroke-linecap='round',
                        stroke-linejoin='round',
                        stroke-width='2',
                        d='M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129'
                    )
                | &nbsp; {{ language }}
</template>

<script>
import { onMounted, ref } from 'vue'
import { useI18n } from '@/plugins/i18n_plugin'

const idiomas = {
    en: 'English',
    'pt-BR': 'Português',
}

export default {
    setup() {
        const language = ref('')
        const i18n = useI18n()

        onMounted(() => {
            for (let lang in navigator.languages) {
                for (let key in idiomas) {
                    if (key.includes(lang)) {
                        set_language(lang)
                        return
                    }
                }
                set_language('en')
            }
        })

        const set_language = (lang) => {
            language.value = idiomas[lang]
            i18n.locale.value = lang
            document.querySelector('html').setAttribute('lang', lang)
        }

        const toogle_lang = () => {
            set_language(i18n.locale.value === 'en' ? 'pt-BR' : 'en')
        }

        return { toogle_lang, i18n, language }
    },
}
</script>
