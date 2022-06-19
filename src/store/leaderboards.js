import wordle from '../api/wordle';
import {
    WORDLE_TODAY_BEGIN,
    WORDLE_TODAY_ERROR,
    WORDLE_TODAY_SUCCESS,
    WORDLE_SHAME_BEGIN,
    WORDLE_SHAME_ERROR,
    WORDLE_SHAME_SUCCESS,
    WORDLE_LEADERS_GUESSES_BEGIN,
    WORDLE_LEADERS_GUESSES_ERROR,
    WORDLE_LEADERS_GUESSES_SUCCESS,
    WORDLE_LEADERS_TIME_BEGIN,
    WORDLE_LEADERS_TIME_SUCCESS,
    WORDLE_LEADERS_TIME_ERROR,
} from './types';


const initialState = {
    wordle: {
        today_loading: false,
        today: [],
        shame_loading: false,
        shame: [],
        total: null,
        leaders: {
            avg_guesses: [],
            avg_guesses_loading: false,
            avg_time: [],
            avg_time_loading: false,
        },
    }
};

const getters = {
    // isAuthenticated: state => !!state.token,
};

const actions = {
    todaysWordles({ commit }) {
        commit(WORDLE_TODAY_BEGIN);
        return wordle.today()
            .then(({ data }) => commit(WORDLE_TODAY_SUCCESS, data))
            .catch((error) => commit(WORDLE_TODAY_ERROR, error.response.data));
    },
    wordleFails({ commit }) {
        commit(WORDLE_SHAME_BEGIN);
        return wordle.shame()
            .then(({ data }) => commit(WORDLE_SHAME_SUCCESS, data))
            .catch((error) => commit(WORDLE_SHAME_ERROR));
    },
    wordleAvgGuesses({ commit }) {
        commit(WORDLE_LEADERS_GUESSES_BEGIN);
        return wordle.guessesLeaders()
            .then(({ data }) => commit(WORDLE_LEADERS_GUESSES_SUCCESS, data))
            .catch((error) => commit(WORDLE_LEADERS_GUESSES_ERROR));
    },
    wordleAvgTime({ commit }) {
        commit(WORDLE_LEADERS_TIME_BEGIN);
        return wordle.timeLeaders()
            .then(({ data }) => commit(WORDLE_LEADERS_TIME_SUCCESS, data))
            .catch((error) => commit(WORDLE_LEADERS_TIME_ERROR));
    },
    // leaders({ commit }) {
    //     commit(WORDLE_LEADERS_BEGIN);
    //     return wordle.guess(guess)
    //         .then(({ data }) => commit(WORDLE_LEADERS_ERROR, data))
    //         .catch((error) => commit(WORDLE_LEADERS_SUCCESS, error.response.data));
    // },
};

const mutations = {
    // Todays Wordle Mutations
    [WORDLE_TODAY_BEGIN](state) {
        state.wordle.today_loading = true
    },
    [WORDLE_TODAY_SUCCESS](state, data) {
        state.wordle.today_loading = false
        state.wordle.today = data
    },
    [WORDLE_TODAY_ERROR](state, error) {
        state.wordle.today_loading = false
    },

    // Wordle Wall of Shame Mutations
    [WORDLE_SHAME_BEGIN](state) {
        state.wordle.shame_loading = true
    },
    [WORDLE_SHAME_SUCCESS](state, data) {
        state.wordle.shame = data
        state.wordle.shame_loading = false
    },
    [WORDLE_SHAME_ERROR](state) {
        state.wordle.shame_loading = false
    },

    // Wordle Leader Guesses Mutations
    [WORDLE_LEADERS_GUESSES_BEGIN](state) {
        state.wordle.leaders.avg_guesses_loading = true
    },
    [WORDLE_LEADERS_GUESSES_SUCCESS](state, data) {
        state.wordle.leaders.avg_guesses_loading = false
        state.wordle.leaders.avg_guesses = data
    },
    [WORDLE_LEADERS_GUESSES_ERROR](state) {
        state.wordle.leaders.avg_guesses_loading = false
    },

    // Wordle Leader Time Mutations
    [WORDLE_LEADERS_TIME_BEGIN](state) {
        state.wordle.leaders.avg_time_loading = true
    },
    [WORDLE_LEADERS_TIME_SUCCESS](state, data) {
        state.wordle.leaders.avg_time_loading = false
        state.wordle.leaders.avg_time = data
    },
    [WORDLE_LEADERS_TIME_ERROR](state) {
        state.wordle.leaders.avg_time_loading = false
    },

};

export default {
    namespaced: true,
    state: initialState,
    getters,
    actions,
    mutations,
};