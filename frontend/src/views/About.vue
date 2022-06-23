<template lang="pug">
</template>

<script>
import { useI18n } from './plugins/i18n_plugin'

export default {
    setup() {
        const i18n = useI18n()

        return { i18n }
    }
}
</script>
