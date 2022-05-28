import axios from 'axios';

const CSRF_COOKIE_NAME = 'csrftoken';
const CSRF_HEADER_NAME = 'X-CSRFToken';

axios.defaults.withCredentials = true;

// In production baseURL and crossdomain should be removed

const session = axios.create({
    baseURL: 'http://converge-general-sports.herokuapp:80',
    header: "Access-Control-Allow-Origin",
    crossdomain: true,
    xsrfCookieName: CSRF_COOKIE_NAME,
    xsrfHeaderName: CSRF_HEADER_NAME,
});

export default session;