import {createRouter, createWebHistory} from 'vue-router';
import Landing from '@/pages/Landing.vue';
import Upload from '@/pages/Upload.vue';
import WebcamTest from './views/WebcamTest.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'landing',
            component: Landing,
        },
        {
        path: '/webcam-test',
        name: 'webcam-test',
        component: WebcamTest,
        },
        {
            path: '/upload',
            name: 'upload',
            component: Upload,
        }
    ],
})

export default router
