import session from './session';

export default {
    guess(guess) {
        return session.post('/wordle/guess/', { guess });
    },
    status() {
        return session.post('/wordle/status/', {});
    },
};