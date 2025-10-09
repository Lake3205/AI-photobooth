import {createRouter, createWebHistory} from 'vue-router';
import Landing from '@/pages/Landing.vue';
import Upload from '@/pages/Upload.vue';
import SelfieCamera from '@/pages/SelfieCamera.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'landing',
            component: Landing,
        },
        {
            path: '/selfie',
            name: 'selfie',
            component: SelfieCamera,
        },
        {
            path: '/upload',
            name: 'upload',
            component: Upload,
        }
    ],
})

export default router
