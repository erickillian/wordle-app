/**
 * pluins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Plugins
import vuetify from './vuetify';
import pinia from '../stores';
import router from '../router';
import ToastPlugin from './toast';

// Pinia persistence plugin
import piniaPersist from 'pinia-plugin-persistedstate';

// Types
import type { App } from 'vue';

export function registerPlugins(app: App) {
    // Add the Pinia persistence plugin
    pinia.use(piniaPersist);
    app
        .use(vuetify)
        .use(router)
        .use(pinia)
        .use(ToastPlugin);
}
