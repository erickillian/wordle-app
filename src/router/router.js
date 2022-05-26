import Vue from 'vue'
import Router from 'vue-router'

import HomeView from '../views/HomeView'
import PlayersView from '../views/PlayersView'
import EventsView from '../views/EventView'
import WordleView from '../views/WordleView';
import NotFoundView from '../views/NotFoundView'
import LoginView from '../views/LoginView';
import LostView from '../views/LostView';
import PasswordResetView from '../views/PasswordResetView';
import PasswordResetConfirmView from '../views/PasswordResetConfirmView';
import RegisterView from '../views/RegisterView';
import VerifyEmailView from '../views/VerifyEmailView';

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
            component: LoginView,
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
            component: PasswordResetView,
        },
        {
            path: '/password_reset/:uid/:token',
            name: 'password_reset_confirm',
            meta: { layout: 'empty-layout' },
            component: PasswordResetConfirmView,
        },
        {
            path: '/register',
            name: 'register',
            meta: { layout: 'empty-layout' },
            component: RegisterView,
        },
        {
            path: '/register/:key',
            name: 'verify_email',
            meta: { layout: 'empty-layout' },
            component: VerifyEmailView,
        },
        {
            path: '/',
            name: 'home',
            meta: { layout: 'main-layout' },
            component: HomeView,
            beforeEnter: requireAuthenticated,
        },
        {
            path: '/players/:id?',
            name: 'players',
            meta: { layout: 'main-layout' },
            component: PlayersView,
            beforeEnter: requireAuthenticated,
        },
        {
            path: '/wordle',
            name: 'wordle',
            meta: { layout: 'main-layout' },
            component: WordleView,
            beforeEnter: requireAuthenticated,
        },
        {
            path: '/events/:id?',
            name: 'events',
            meta: { layout: 'main-layout' },
            component: EventsView,
            beforeEnter: requireAuthenticated,
        },
        { path: '/404', meta: { layout: 'empty-layout' }, component: NotFoundView },
        { path: '*', redirect: '/404' }
    ]
})
