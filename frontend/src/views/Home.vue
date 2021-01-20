<template lang="pug">
.main
    div
        .languages
            h1 Languages
        .editor
            h1 Editor
</template>

<script>
</script>

<style lang="stylus" scoped>

.main
    height 100%
    div
        display grid
        grid-template-columns 1fr 3fr
        grid-gap 1rem
    .languages
        background-color blue
    .editor
        background-color #222

</style>
