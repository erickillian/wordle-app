import wordle from '../api/wordle';
import session from '../api/session';
import {
    WORDLE_STATUS_BEGIN,
    WORDLE_STATUS_ERROR,
    WORDLE_STATUS_SUCCESS,
    WORDLE_GUESS_BEGIN,
    WORDLE_GUESS_ERROR,
    WORDLE_GUESS_SUCCESS,
} from './types';


const initialState = {
    guess: '',
    correct: '',
    // registration_error: {
    //     username: '',
    //     firstname: '',
    //     lastname: '',
    //     email: '',
    //     password1: '',
    //     password2: '',
    // },
    // login_error: {
    //     username: '',
    //     password: ''
    // }
};

const getters = {
    // isAuthenticated: state => !!state.token,
};

const actions = {
    status({ commit }) {
        commit(WORDLE_STATUS_BEGIN);
        return wordle.status(username, password)
            .then(({ data }) => commit(WORDLE_STATUS_SUCCESS, data))
            .catch((error) => commit(WORDLE_STATUS_ERROR, error.response.data));
    },
    guess({ commit }, { guess }) {
        commit(WORDLE_GUESS_BEGIN);
        return wordle.guess(username, password)
            .then(({ data }) => commit(WORDLE_GUESS_SUCCESS, data))
            .catch((error) => commit(WORDLE_GUESS_ERROR, error.response.data));
    },
};

const mutations = {
    [WORDLE_STATUS_BEGIN](state) {

    },
    [WORDLE_STATUS_SUCCESS](state, data) {
        console.log(data)
    },
    [WORDLE_STATUS_ERROR](state, error) {
        console.log(error)
    },
    [WORDLE_GUESS_BEGIN](state) {

    },
    [WORDLE_GUESS_SUCCESS](state, data) {
        console.log(data)
    },
    [WORDLE_GUESS_ERROR](state, error) {
        console.log(error)
    },
};

export default {
    namespaced: true,
    state: initialState,
    getters,
    actions,
    mutations,
};