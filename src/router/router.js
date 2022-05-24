import Vue from 'vue'
import Router from 'vue-router'

import Home from '../views/Home.vue'
import Players from '../views/Players.vue'
import Events from '../views/Events.vue'
import Wordle from '../views/Wordle';
import NotFound from '../views/NotFound.vue'
import Login from '../views/Login';
import Lost from '../views/Lost';
import PasswordReset from '../views/PasswordReset';
import PasswordResetConfirm from '../views/PasswordResetConfirm';
import Register from '../views/Register';
import VerifyEmail from '../views/VerifyEmail';

import store from '../store/store';

Vue.use(Router)

const requireAuthenticated = (to, from, next) => {
    store.dispatch('auth/initialize')
        .then(() => {
            if (!store.getters['auth/isAuthenticated']) {
                next('/login');
            } else {
                next();
            }
        });
};

const requireUnauthenticated = (to, from, next) => {
    store.dispatch('auth/initialize')
        .then(() => {
            if (store.getters['auth/isAuthenticated']) {
                next('/');
            } else {
                next();
            }
        });
};

const redirectLogout = (to, from, next) => {
    store.dispatch('auth/logout')
        .then(() => next('/login'));
};

export default new Router({
    mode: 'history',
    // base: process.env.BASE_URL,
    routes: [
        {
            path: '/login',
            name: 'login',
            meta: { layout: 'empty-layout' },
            component: Login,
            beforeEnter: requireUnauthenticated,
        },
        {
            path: '/logout',
            name: 'logout',
            meta: { layout: 'empty-layout' },
            beforeEnter: redirectLogout,
        },
        {
            path: '/password_reset',
            name: 'password_reset',
            meta: { layout: 'empty-layout' },
            component: PasswordReset,
        },
        {
            path: '/password_reset/:uid/:token',
            name: 'password_reset_confirm',
            meta: { layout: 'empty-layout' },
            component: PasswordResetConfirm,
        },
        {
            path: '/register',
            name: 'register',
            meta: { layout: 'empty-layout' },
            component: Register,
        },
        {
            path: '/register/:key',
            name: 'verify_email',
            meta: { layout: 'empty-layout' },
            component: VerifyEmail,
        },
        {
            path: '/',
            name: 'home',
            meta: { layout: 'main-layout' },
            component: Home,
            beforeEnter: requireAuthenticated,
        },
        {
            path: '/players/:id?',
            name: 'players',
            meta: { layout: 'main-layout' },
            component: Players,
            beforeEnter: requireAuthenticated,
        },
        {
            path: '/wordle',
            name: 'wordle',
            meta: { layout: 'main-layout' },
            component: Wordle,
            beforeEnter: requireAuthenticated,
        },
        {
            path: '/events/:id?',
            name: 'events',
            meta: { layout: 'main-layout' },
            component: Events,
            beforeEnter: requireAuthenticated,
        },
        { path: '/404', meta: { layout: 'empty-layout' }, component: NotFound },
        { path: '*', redirect: '/404' }
    ]
})
