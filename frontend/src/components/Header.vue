<template lang="pug">
header.main
    section
        h1.logotipo
            router-link(to="/") Code Lab
        nav
            span(@click="toogle_lang", style="cursor: pointer")
                svg.icon(
                    fill="none",
                    stroke="currentColor",
                    viewBox="0 0 24 24"
                )
                    path(
                        d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129",
                        stroke-linecap="round",
                        stroke-linejoin="round",
                        stroke-width="2"
                    )
                | &nbsp; {{ language }}
</template>

<script setup>
import { computed, inject } from "vue"

const idiomas = {
    en: "English",
    "pt-BR": "Português",
}

const i18n = inject('i18n')

function set_language(lang) {
    i18n.locale.value = lang
    document.querySelector("html").setAttribute("lang", lang)
}

function toogle_lang() {
    set_language(i18n.locale.value === "en" ? "pt-BR" : "en")
}

const language = computed(() => idiomas[i18n.locale.value === "en" ? "pt-BR" : "en"]);
</script>
