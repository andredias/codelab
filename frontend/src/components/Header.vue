<template lang="pug">
header.main
    section
        h1.logotipo
            router-link(to="/") Code Lab
        nav
            router-link(to="/") {{ i18n.$t('home') }}
            router-link(to="/dojo") Dojo
            router-link(to="/how") {{ i18n.$t('how_it_works') }}
            span(@click="toogle_lang" style="cursor: pointer")
                svg.icon(
                    fill="none",
                    viewBox="0 0 24 24",
                    stroke="currentColor"
                )
                    path(
                        stroke-linecap="round",
                        stroke-linejoin="round",
                        stroke-width="2",
                        d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"
                    )
                | &nbsp; {{ language }}
</template>

<script>
import { onMounted, ref } from "vue";
import { useI18n } from "@/plugins/i18n_plugin";

const idiomas = {
    en: "English",
    "pt-BR": "Português",
};

export default {
    setup() {
        const language = ref("");
        const i18n = useI18n();

        onMounted(() => {
            for (let lang in navigator.languages) {
                for (let key in idiomas) {
                    if (key.includes(lang)) {
                        set_language(lang);
                        return;
                    }
                }
                set_language("en");
            }
        });

        const set_language = (lang) => {
            language.value = idiomas[lang]
            i18n.locale.value = lang;
            document.querySelector("html").setAttribute("lang", lang);
        };

        const toogle_lang = () => {
            set_language(i18n.locale.value === "en" ? "pt-BR" : "en");
        };

        return { toogle_lang, i18n, language };
    },
};
</script>
