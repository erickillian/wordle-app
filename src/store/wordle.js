import wordle from '../api/wordle';
import {
    WORDLE_STATUS_BEGIN,
    WORDLE_STATUS_ERROR,
    WORDLE_STATUS_SUCCESS,
    WORDLE_GUESS_BEGIN,
    WORDLE_GUESS_ERROR,
    WORDLE_GUESS_SUCCESS,
    WORDLE_GUESS_RESPONDED,
    WORDLE_STATS_BEGIN,
    WORDLE_STATS_ERROR,
    WORDLE_STATS_SUCCESS,
} from './types';


const initialState = {
    initial_load: false,
    status_loading: true,
    status_error: false,
    guess_loading: false,
    guess_error: false,
    guess_ok: false,
    guess_error: false,
    info: {
        guesses: 0,
        guess_history: '',
        solved: false,
        start_time: '',
        correct: '',
    },
    errors: {},
    stats_loading: false,
    stats: {
        num_wordles: 0,
        num_players: 0,
    },
};

const getters = {
    // isAuthenticated: state => !!state.token,
};

const actions = {
    status({ commit }) {
        commit(WORDLE_STATUS_BEGIN);
        return wordle.status()
            .then(({ data }) => commit(WORDLE_STATUS_SUCCESS, data))
            .catch((error) => commit(WORDLE_STATUS_ERROR, error.response.data));
    },
    guess({ commit }, { guess }) {
        commit(WORDLE_GUESS_BEGIN);
        return wordle.guess(guess)
            .then(({ data }) => commit(WORDLE_GUESS_SUCCESS, data))
            .catch((error) => commit(WORDLE_GUESS_ERROR, error.response.data));
    },
    stats({ commit }) {
        commit(WORDLE_STATS_BEGIN);
        return wordle.stats()
            .then(({ data }) => commit(WORDLE_STATS_SUCCESS, data))
            .catch((error) => commit(WORDLE_STATS_ERROR, error.response.data));
    },
};

const mutations = {
    [WORDLE_STATS_BEGIN](state) {
        state.stats_loading = true
        state.stats_error = false
    },
    [WORDLE_STATS_SUCCESS](state, data) {
        state.stats_loading = false
        state.stats_error = false
        state.stats = data
    },
    [WORDLE_STATS_ERROR](state, error) {
        state.stats_error = true
        state.stats_loading = false
    },

    [WORDLE_STATUS_BEGIN](state) {
        state.initial_load = false
        state.status_loading = true
        state.status_error = false
    },
    [WORDLE_STATUS_SUCCESS](state, data) {
        state.initial_load = true
        state.status_loading = false
        state.status_error = false
        state.info = data
    },
    [WORDLE_STATUS_ERROR](state, error) {
        state.status_error = true
        state.status_loading = false
    },
    [WORDLE_GUESS_BEGIN](state) {
        state.guess_loading = true
        state.guess_error = false
    },
    [WORDLE_GUESS_SUCCESS](state, data) {
        state.guess_ok = true
        state.guess_loading = false
        state.guess_error = false
        state.info = data
    },
    [WORDLE_GUESS_RESPONDED](state) {
        state.guess_ok = false
        state.guess_error = false
    },
    [WORDLE_GUESS_ERROR](state, error) {
        state.guess_error = true
        state.guess_loading = false
        state.guess_error = true
        state.errors = error
    },
};

export default {
    namespaced: true,
    state: initialState,
    getters,
    actions,
    mutations,
};