<template lang="pug">
.home.miolo
    section.hero
        h1.logo Code Lab
        h2 {{ i18n.$t('hero_msg') }}

    //- section.languages
    //-     header
    //-         nav.tab
    //-             button(
    //-                 :class="selected_lang === 'all' ? 'active' : ''",
    //-                 @click="selected_lang = 'all'"
    //-             ) {{ i18n.$t('all_languages') }}
    //-             button(
    //-                 :class="selected_lang === lang ? 'active' : ''",
    //-                 :key="lang",
    //-                 @click="select_language(lang)",
    //-                 v-for="lang in languages"
    //-             ) {{ lang }}
    //-         .toolbar.flex-justify
    //-             select(v-model="new_project_language")
    //-                 option(v-for="lang in languages") {{ lang }}
    //-             button.btn.btn-secondary.btn-slim(
    //-                 @click="router.push(`/dojo/new/${new_project_language}`)"
    //-             ) {{ i18n.$t('new_project') }}
    //-     .content
    //-         project(
    //-             :key="index",
    //-             v-bind="project",
    //-             v-for="(project, index) in projects"
    //-         )
</template>

<script setup>
import { inject, ref, onMounted } from "vue"
// import project from "./components/project"
import axios from "axios"
import { useRouter } from "vue-router"

const i18n = inject('i18n')
const languages = ["Python"]
const selected_lang = ref("all")
const projects = ref([])
const router = useRouter()
const new_project_language = ref("Python")

// onMounted(async () => {
//     let data = (await axios.get(`${process.env.VUE_APP_API_URL}/projects`))
//         .data
//     data.map((project) => (project.timestamp = new Date(project.timestamp)))
//     projects.value = data.sort(
//         (a, b) =>
//             Math.floor(b.timestamp / 1000) - Math.floor(a.timestamp / 1000) || // ignores miliseconds
//             a.title.localeCompare(b.title)
//     )
// })

// function select_language(lang) {
//     selected_lang.value = lang
//     new_project_language.value = lang
// }
</script>
