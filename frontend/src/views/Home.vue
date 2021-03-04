<template lang="pug">
.home
    section.hero
        h1.logo Code Lab
        h2 {{ i18n.$t("hero_msg") }}

    section.languages
        header
            nav.tab
                button(
                    :class='selected_lang === "all" ? "active" : ""'
                    @click='selected_lang = "all"'
                ) {{ i18n.$t("all_languages") }}
                button(
                    :class='selected_lang === lang ? "active" : ""'
                    :key='lang'
                    @click='selected_lang = lang'
                    v-for='lang in languages'
                ) {{ lang }}
            .toolbar
                button(:enabled='selected_lang !== "all"') New
        .content
            project(:key='index' v-bind='project' v-for='(project, index) in projects')
</template>

<script>
import { ref, onMounted } from 'vue'
import { useI18n } from '@/plugins/i18n_plugin'
import project from '@/components/project'
import axios from 'axios'

export default {
    components: {
        project,
    },
    setup() {
        const i18n = useI18n()
        const languages = ['Python', 'Go', 'Rust']
        const selected_lang = ref('all')
        const projects = ref([])

        onMounted(async () => {
            let data = (await axios.get(`${process.env.VUE_APP_API_URL}/projects`)).data
            data.map((project) => (project.timestamp = new Date(project.timestamp)))
            projects.value = data.sort(
                (a, b) =>
                    Math.floor(b.timestamp / 1000) - Math.floor(a.timestamp / 1000) || // ignores miliseconds
                    a.title.localeCompare(b.title)
            )
        })

        return {
            i18n,
            languages,
            projects,
            selected_lang,
        }
    },
}
</script>
