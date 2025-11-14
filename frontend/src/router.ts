import {createRouter, createWebHistory} from 'vue-router';
import { authService } from '@/services/authService';
import Login from '@/pages/Login.vue';
import Landing from '@/pages/Landing.vue';
import SelfieCamera from '@/pages/SelfieCamera.vue';
import Dashboard from '@/pages/Dashboard.vue';
import TermsOfService from '@/pages/TermsOfService.vue';

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
            path: '/login',
            name: 'login',
            component: Login,
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: Dashboard,
            meta: { requiresAuth: true, requiredRole: 'admin' }
        },
        {
            path: '/terms-of-service',
            name: 'terms-of-service',
            component: TermsOfService,
        },
        {
            path: '/form',
            name: 'form',
            component: () => import('@/pages/Form.vue'),
            meta: { requiresToken: true }
        }
    ],
})


// JWT-based route guard
router.beforeEach(async (to, _from, next) => {
    if (to.meta.requiresAuth) {
        const isAuthenticated = authService.isAuthenticated()
        
        if (!isAuthenticated) {
            next('/login')
            return
        }
        
        // Verify token with backend
        const isValid = await authService.verifyToken()
        if (!isValid) {
            next('/login')
            return
        }
    }

    if (to.meta.requiresToken) {
        const token = to.query.token as string | undefined;
        
        if (!token) {
            next('/');
            return;
        }

        const isValidToken = await authService.verifyFormToken(token);
        if (!isValidToken) {
            next('/');
            return;
        }
    }
    
    next()
})

export default router
