import {createRouter, createWebHistory} from 'vue-router';
import { authService } from '@/services/authService';
import Login from '@/pages/Login.vue';
import SelfieCamera from '@/pages/SelfieCamera.vue';
import Dashboard from '@/pages/Dashboard.vue';
import PhotoBooth from './pages/PhotoBooth.vue';
import TermsOfService from '@/pages/TermsOfService.vue';
import { useCookieService } from './services/cookieService';


const { getCookie } = useCookieService();

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'selfie',
            component: SelfieCamera,
        },
        {
            path:'/booth',
            name:'photobooth',
            component: PhotoBooth,
            meta: { requiresAuth: true, requiredRole: 'admin' }
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
            // Save the intended destination
            localStorage.setItem('redirectAfterLogin', to.fullPath)
            next('/login')
            return
        }
        
        // Verify token with backend
        const isValid = await authService.verifyToken()
        if (!isValid) {
            // Save the intended destination
            localStorage.setItem('redirectAfterLogin', to.fullPath)
            next('/login')
            return
        }
    }

    if (to.meta.requiresToken) {
        let token = to.query.token as string | undefined;

        if (!token) {
            token = getCookie('form_token');
        }
        
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
