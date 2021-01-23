<template lang="pug">
.dojo
    .header-container
        header
            div
                h3.bread-crumbs
                    router-link(to="/") Home
                    router-link(to="/languages/python") Python
                    span Título do Projeto

    main
        div.descricao
            div.edit
                <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
            h1 Título do Projeto
            p Deploy web apps of all kinds, from large scale enterprise APIs to static websites for individuals. Fill out the form to try a demo of our platform
        div.stats
            h1 Estatísticas

        div.editor
            codemirror(v-model="code")

        div.input-output
            h1 Run

</template>

<script>
import codemirror from '@/components/codemirror'
import { ref } from 'vue'

export default {
    components: {
        codemirror,
    },
    setup() {
        const code = ref('teste 123')
        return { code }
    }

}
</script>
