import {createRouter, createWebHistory} from 'vue-router';
import Landing from '@/pages/Landing.vue';
import Upload from '@/pages/Upload.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'landing',
            component: Landing,
        },
        {
            path: '/upload',
            name: 'upload',
            component: Upload,
        }
    ],
})

export default router
