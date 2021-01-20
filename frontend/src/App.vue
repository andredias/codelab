<template lang="pug">
Header
router-view
Footer
</template>

<script>
import Header from "./components/Header"
import Footer from "./components/Footer"
export default {
    name: "Code Lab",
    components: {
        Header,
        Footer
    }
}
</script>
