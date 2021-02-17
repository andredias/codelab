import {createRouter, createWebHistory} from 'vue-router'
import Home from '../views/Home'
import Dojo from '../views/Dojo'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/about',
        name: 'About',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import(/* webpackChunkName: "about" */ '../views/About')
    },
    {
        path: '/dojo',
        name: 'Dojo',
        component: Dojo
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
