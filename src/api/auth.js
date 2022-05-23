import session from './session';

export default {
    login(username, password) {
        return session.post('/auth/login/', { username, password });
    },
    logout() {
        return session.post('/auth/logout/', {});
    },
    createAccount(username, firstname, lastname, email, password1, password2) {
        return session.post('/auth/registration/', { username, firstname, lastname, email, password1, password2 });
    },
    changeAccountPassword(password1, password2) {
        return session.post('/auth/password/change/', { password1, password2 });
    },
    sendAccountPasswordResetEmail(email) {
        return session.post('/auth/password/reset/', { email });
    },
    resetAccountPassword(uid, token, new_password1, new_password2) { // eslint-disable-line camelcase
        return session.post('/auth/password/reset/confirm/', { uid, token, new_password1, new_password2 });
    },
    getAccountDetails() {
        return session.get('/auth/user/');
    },
    updateAccountDetails(data) {
        return session.patch('/auth/user/', data);
    },
    verifyAccountEmail(key) {
        return session.post('/auth/registration/verify-email/', { key });
    },
};