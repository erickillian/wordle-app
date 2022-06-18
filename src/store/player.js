import player from '../api/player';
import i18n from '../i18n'


import {
    PLAYER_WORDLE_STATS_BEGIN,
    PLAYER_WORDLE_STATS_ERROR,
    PLAYER_WORDLE_STATS_SUCCESS,
    PLAYER_WORDLES_BEGIN,
    PLAYER_WORDLES_ERROR,
    PLAYER_WORDLES_SUCCESS,
    PLAYER_GUESS_DISTRIBUTION_BEGIN,
    PLAYER_GUESS_DISTRIBUTION_ERROR,
    PLAYER_GUESS_DISTRIBUTION_SUCCESS,
    PLAYER_ALL_BEGIN,
    PLAYER_ALL_ERROR,
    PLAYER_ALL_SUCCESS,
    SELECT_PLAYER,
    PLAYER_NOT_FOUND,
} from './types';


const initialState = {
    all_loading: false,
    all_error: false,
    all: [],
    all_columns: [
        { text: i18n.t("players_list.name_col"), value: "full_name", width: 180 },
        { text: i18n.t("players_list.avg_guess_col"), value: 'avg_guesses', width: 100 },
    ],

    selected_id: null,
    not_found: false,

    stats_loading: true,
    stats_error: false,
    stats: {},

    guess_distribution_loading: true,
    guess_distribution_error: false,
    guess_distribution: {},

    wordles_loading: true,
    wordles_error: false,
    wordles: [],

    matchHistoryColumns: [
        { text: i18n.t('player_card.history.cols.id'), value: "id", width: "10%" },
        { text: i18n.t('player_card.history.cols.match_date'), value: "datetime", width: "30%" },
        { text: i18n.t('player_card.history.cols.score'), value: "score", width: "30%" },
        { text: i18n.t('player_card.history.cols.opponent_name'), value: "opponent_name", width: "30%" },
    ]
};

const getters = {
    // isAuthenticated: state => !!state.token,
};

const actions = {
    all({ commit }) {
        commit(PLAYER_ALL_BEGIN);
        return player.all()
            .then(({ data }) => commit(PLAYER_ALL_SUCCESS, data))
            .catch((error) => commit(PLAYER_ALL_ERROR, error.response.data));
    },
    wordles({ commit }, player_id) {
        if (player_id === undefined) {
            console.log("Undefined")
            commit(PLAYER_NOT_FOUND);
        } else {
            console.log("Getting Wordles")
            commit(PLAYER_WORDLES_BEGIN);
            return player.wordles(player_id)
                .then(({ data }) => commit(PLAYER_WORDLES_SUCCESS, data))
                .catch((error) => commit(PLAYER_WORDLES_ERROR, error.response.data))
        }
    },
    guessDistribution({ commit }, player_id) {
        if (player_id === undefined) {
            commit(PLAYER_NOT_FOUND);
        } else {
            console.log("Getting Guess Distribution")
            commit(PLAYER_GUESS_DISTRIBUTION_BEGIN);
            return player.guess_distribution(player_id)
                .then(({ data }) => commit(PLAYER_GUESS_DISTRIBUTION_SUCCESS, data))
                .catch((error) => commit(PLAYER_GUESS_DISTRIBUTION_ERROR, error.response.data))
        }
    },
    stats({ commit }, player_id) {
        if (player_id === undefined) {
            commit(PLAYER_NOT_FOUND);
        } else {
            commit(SELECT_PLAYER, player_id);
            commit(PLAYER_WORDLE_STATS_BEGIN);
            return player.stats(player_id)
                .then(({ data }) => commit(PLAYER_WORDLE_STATS_SUCCESS, data))
                .catch((error) => commit(PLAYER_WORDLE_STATS_ERROR, error.response.data))
        }
    },
};

const mutations = {
    [PLAYER_NOT_FOUND](state, player_id) {
        state.not_found = true
    },
    [SELECT_PLAYER](state, player_id) {
        state.selected_id = player_id
    },
    [PLAYER_WORDLE_STATS_BEGIN](state) {
        state.stats = {}
        state.stats_loading = true
    },
    [PLAYER_WORDLE_STATS_SUCCESS](state, data) {
        state.stats_loading = false
        state.stats_error = false
        state.stats = data
    },
    [PLAYER_WORDLE_STATS_ERROR](state, error) {
        state.stats_error = true
        state.stats_loading = false
    },
    [PLAYER_WORDLES_BEGIN](state) {
        state.wordles = []
        state.wordles_loading = true
    },
    [PLAYER_WORDLES_SUCCESS](state, data) {
        state.wordles_loading = false
        state.wordles_error = false
        state.wordles = data
    },
    [PLAYER_WORDLES_ERROR](state, error) {
        state.wordles_error = true
        state.wordles_loading = false
    },
    [PLAYER_GUESS_DISTRIBUTION_BEGIN](state) {
        state.guess_distribution = {}
        state.guess_distribution_loading = true
    },
    [PLAYER_GUESS_DISTRIBUTION_SUCCESS](state, data) {
        state.guess_distribution_loading = false
        state.guess_distribution_error = false
        state.guess_distribution = data
    },
    [PLAYER_GUESS_DISTRIBUTION_ERROR](state, error) {
        state.guess_distribution_error = true
        state.guess_distribution_loading = false
    },
    [PLAYER_ALL_BEGIN](state) {
        state.all_loading = true
    },
    [PLAYER_ALL_SUCCESS](state, data) {
        state.all_loading = false
        state.all_error = false
        state.all = data
    },
    [PLAYER_ALL_ERROR](state, error) {
        state.all_error = true
        state.all_loading = false
    },
};

export default {
    namespaced: true,
    state: initialState,
    getters,
    actions,
    mutations,
};