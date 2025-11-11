import {createRouter, createWebHistory} from 'vue-router';
import Landing from '@/pages/Landing.vue';
import SelfieCamera from '@/pages/SelfieCamera.vue';
import Dashboard from '@/pages/Dashboard.vue';
import Login from '@/pages/Login.vue';
import { authService } from '@/services/authService';

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
    
    next()
})

export default router
