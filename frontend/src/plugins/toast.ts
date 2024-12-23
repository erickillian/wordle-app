// toast.ts
import { reactive } from 'vue';

export default {
    install(app: any) {
        const toastState = reactive({
            show: false,
            message: '',
            color: 'success',
            timeout: 3000,
        });

        const showToast = (message: string, color: string = 'success', timeout: number = 3000) => {
            toastState.show = true;
            toastState.message = message;
            toastState.color = color;
            toastState.timeout = timeout;
        };

        const toast = {
            success(message: string, timeout: number = 3000) {
                showToast(message, 'success', timeout);
            },
            error(message: string, timeout: number = 3000) {
                showToast(message, 'error', timeout);
            },
            info(message: string, timeout: number = 3000) {
                showToast(message, 'info', timeout);
            },
        };

        app.config.globalProperties.$toast = toast;

        app.provide('toastState', toastState);
    },
};