<template>
    <v-app>
        <NavBarComponent />
        <v-main>
            <router-view />
        </v-main>
        <v-snackbar v-model="toastState.show" :timeout="toastState.timeout" :color="toastState.color">
            {{ toastState.message }}
        </v-snackbar>
    </v-app>
</template>

<script lang="ts">
import { defineComponent, inject } from 'vue';
import NavBarComponent from '@/components/NavBarComponent.vue';

export default defineComponent({
    name: 'InternalLayout',
    components: {
        NavBarComponent,
    },
    setup() {
        const toastState = inject<{ show: boolean; timeout: number; color: string; message: string }>('toastState', {
            show: false,
            timeout: 3000,
            color: '',
            message: ''
        });
        const route = useRoute();
        return { toastState, route };
    },
});
</script>

<style scoped>
/* Add styles if needed */
</style>