import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            // vue alias solve a problem with the current vue-router version
            // [Vue warn]: Component provided template option but runtime compilation is not supported in this build of Vue. Configure your bundler to alias "vue" to "vue/dist/vue.esm-bundler.js".
            // see also: https://github.com/vuejs/router/issues/858#issuecomment-823961788
            'vue': 'vue/dist/vue.esm-bundler.js',
        }
    }
})
