import session from './session';

export default {
    all() {
        return session.get(`/api/v1/players/all`);
    },
    stats(player_id) {
        return session.get(`/api/v1/player/${player_id}/wordle/stats`);
    },
    wordles(player_id) {
        return session.get(`/api/v1/player/${player_id}/wordles`);
    },
};