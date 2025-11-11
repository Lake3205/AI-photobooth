import {createRouter, createWebHistory} from 'vue-router';
import Landing from '@/pages/Landing.vue';
import SelfieCamera from '@/pages/SelfieCamera.vue';
import Dashboard from '@/pages/Dashboard.vue';
import TermsOfService from "@/pages/TermsOfService.vue";

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
            path: '/dashboard',
            name: 'dashboard',
            component: Dashboard,
        },
        {
            path: '/terms-of-service',
            name: 'terms-of-service',
            component: TermsOfService,
        },
    ],
})

export default router
