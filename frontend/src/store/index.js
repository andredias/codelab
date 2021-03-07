import { createStore } from "vuex"
import axios from 'axios'

export default createStore({
    state: {
        projects: [],
    },
    mutations: {
        include(project) {
            if (!state.projects.filter(proj => proj.id === project.id)) {
                state.projects.push(project)
            }
        }
    },
    actions: {

    },
    modules: {}
})
