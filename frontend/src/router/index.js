import { createRouter, createWebHistory } from 'vue-router'
import Dojo from '../views/Dojo.vue'

const routes = [
    {
        path: '/',
        component: Dojo
    },
    {
        path: '/dojo',
        component: Dojo
    },
    {
        path: '/dojo/:id',
        name: 'Dojo',
        component: Dojo,
    },
    {
        path: '/about',
        name: 'About',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import(/* webpackChunkName: "about" */ '../views/About.vue')
    },
    {
        path: '/terms_of_use',
        name: 'TermsOfUse',
        component: () =>
            import('../views/terms_of_use.vue')
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
