import session from './session';

export default {
    guess(guess) {
        return session.post('api/v1/wordle/guess', { guess });
    },
    status() {
        return session.get('api/v1/wordle/status', {});
    },
    today() {
        return session.get('api/v1/wordle/today', {});
    },
    shame() {
        return session.get('api/v1/wordle/shame', {});
    },
    guessesLeaders() {
        return session.get('api/v1/wordle/leaders/guesses', {});
    },
    timeLeaders() {
        return session.get('api/v1/wordle/leaders/time', {});
    },
};