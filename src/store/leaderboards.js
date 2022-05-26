import wordle from '../api/wordle';
import {
    WORDLE_TODAY_BEGIN,
    WORDLE_TODAY_ERROR,
    WORDLE_TODAY_SUCCESS,
    WORDLE_LEADERS_BEGIN,
    WORDLE_LEADERS_ERROR,
    WORDLE_LEADERS_SUCCESS,
} from './types';


const initialState = {
    wordle: {
        today_loading: false,
        leaders_loading: false,
        today: [],
        leaders: {
        }
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
    fetchLeaderboard(context) {

    }
    // leaders({ commit }) {
    //     commit(WORDLE_LEADERS_BEGIN);
    //     return wordle.guess(guess)
    //         .then(({ data }) => commit(WORDLE_LEADERS_ERROR, data))
    //         .catch((error) => commit(WORDLE_LEADERS_SUCCESS, error.response.data));
    // },
};

const mutations = {
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
    [WORDLE_LEADERS_BEGIN](state) {
        state.wordle.leaders_loading = true
    },
    [WORDLE_LEADERS_SUCCESS](state, data) {
        state.wordle.leaders_loading = false
    },
    [WORDLE_LEADERS_ERROR](state, error) {
        state.wordle.leaders_loading = false
    },
};

export default {
    namespaced: true,
    state: initialState,
    getters,
    actions,
    mutations,
};