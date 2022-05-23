import auth from '../api/auth';
import session from '../api/session';
import {
    LOGIN_BEGIN,
    LOGIN_ERROR,
    LOGIN_SUCCESS,
    LOGOUT,
    REMOVE_TOKEN,
    SET_TOKEN,
    ACTIVATION_BEGIN,
    ACTIVATION_CLEAR,
    ACTIVATION_ERROR,
    ACTIVATION_SUCCESS,
    REGISTRATION_BEGIN,
    REGISTRATION_CLEAR,
    REGISTRATION_ERROR,
    REGISTRATION_SUCCESS,
} from './types';

const TOKEN_STORAGE_KEY = 'TOKEN_STORAGE_KEY';
const isProduction = false; //process.env.NODE_ENV === 'production';

const initialState = {
    authenticating: false,
    error: false,
    token: null,
    activationCompleted: false,
    activationError: false,
    activationLoading: false,
    loginError: false,
    loginLoading: false,
    registrationCompleted: false,
    registrationError: false,
    registrationLoading: false,
    registration_error: {
        username: '',
        firstname: '',
        lastname: '',
        email: '',
        password1: '',
        password2: '',
    },
    login_error: {
        username: '',
        password: ''
    }
};

const getters = {
    isAuthenticated: state => !!state.token,
};

const actions = {
    login({ commit }, { username, password }) {
        commit(LOGIN_BEGIN);
        return auth.login(username, password)
            .then(({ data }) => commit(SET_TOKEN, data.key))
            .then(() => commit(LOGIN_SUCCESS))
            .catch((error) => commit(LOGIN_ERROR, error.response.data));
    },
    logout({ commit }) {
        return auth.logout()
            .then(() => commit(LOGOUT))
            .finally(() => commit(REMOVE_TOKEN));
    },
    initialize({ commit }) {
        const token = localStorage.getItem(TOKEN_STORAGE_KEY);

        if (isProduction && token) {
            commit(REMOVE_TOKEN);
        }

        if (!isProduction && token) {
            commit(SET_TOKEN, token);
        }
    },
    createAccount({ commit }, { username, firstname, lastname, email, password1, password2 }) {
        commit(REGISTRATION_BEGIN);
        return auth.createAccount(username, firstname, lastname, email, password1, password2)
            .then(() => commit(REGISTRATION_SUCCESS))
            .catch((error) => commit(REGISTRATION_ERROR, error.response.data));
    },
    activateAccount({ commit }, { key }) {
        commit(ACTIVATION_BEGIN);
        return auth.verifyAccountEmail(key)
            .then(() => commit(ACTIVATION_SUCCESS))
            .catch(() => commit(ACTIVATION_ERROR));
    },
    clearRegistrationStatus({ commit }) {
        commit(REGISTRATION_CLEAR);
    },
    clearActivationStatus({ commit }) {
        commit(ACTIVATION_CLEAR);
    },
};

const mutations = {
    [LOGIN_BEGIN](state) {
        state.authenticating = true;
        state.error = false;
    },
    [LOGIN_ERROR](state, error) {
        state.authenticating = false;
        state.error = true;
        state.login_error.username = error.username;
        state.login_error.password = error.password;
    },
    [LOGIN_SUCCESS](state) {
        state.authenticating = false;
        state.error = false;
    },
    [LOGOUT](state) {
        state.authenticating = false;
        state.error = false;
    },
    [SET_TOKEN](state, token) {
        if (!isProduction) localStorage.setItem(TOKEN_STORAGE_KEY, token);
        session.defaults.headers.Authorization = `Token ${token}`;
        state.token = token;
    },
    [REMOVE_TOKEN](state) {
        localStorage.removeItem(TOKEN_STORAGE_KEY);
        delete session.defaults.headers.Authorization;
        state.token = null;
    },
    [ACTIVATION_BEGIN](state) {
        state.activationLoading = true;
    },
    [ACTIVATION_CLEAR](state) {
        state.activationCompleted = false;
        state.activationError = false;
        state.activationLoading = false;
    },
    [ACTIVATION_ERROR](state) {
        state.activationError = true;
        state.activationLoading = false;
    },
    [ACTIVATION_SUCCESS](state) {
        state.activationCompleted = true;
        state.activationError = false;
        state.activationLoading = false;
    },
    [REGISTRATION_BEGIN](state) {
        state.registrationLoading = true;
    },
    [REGISTRATION_CLEAR](state) {
        state.registrationCompleted = false;
        state.registrationError = false;
        state.registrationLoading = false;
    },
    [REGISTRATION_ERROR](state, error) {
        console.log(error);
        state.registrationError = true;
        state.registrationLoading = false;
        state.registration_error.username = error.username;
        state.registration_error.firstname = error.firstname;
        state.registration_error.lastname = error.lastname;
        state.registration_error.email = error.email;
        state.registration_error.password1 = error.password1;
        state.registration_error.password2 = error.password2;
    },
    [REGISTRATION_SUCCESS](state) {
        state.registrationCompleted = true;
        state.registrationError = false;
        state.registrationLoading = false;
    },
};

export default {
    namespaced: true,
    state: initialState,
    getters,
    actions,
    mutations,
};