<template>
    <div>
        <v-app-bar dense app extended extension-height="0" :elevation="0" :clipped-left="true">
            <v-toolbar-title>Wordle</v-toolbar-title>
            <v-spacer></v-spacer>

            <!-- Mobile Menu Toggle (visible only on small screens) -->
            <v-btn icon @click="toggleDrawer" class="d-md-none">
                <v-icon>mdi-menu</v-icon>
            </v-btn>

            <!-- Desktop Menu Items (visible only on large screens) -->
            <v-toolbar-items class="d-none d-md-flex">
                <v-list-item>
                    <!-- Dropdown Menu -->
                    <v-menu v-model="menuVisible" offset-y :close-on-content-click="false"
                        @click-outside="menuVisible = false" transition="none" transition-duration="0" open-delay="0"
                        close-delay="0" :eager="true">
                        <template v-slot:activator="{ props: activatorProps }">
                            <v-btn icon v-bind="activatorProps">
                                <v-img v-if="user?.profile_picture" :src="user.profile_picture" alt="Profile Picture"
                                    width="46" height="46" />
                            </v-btn>
                        </template>
                        <v-card rounded="lg" min-width="400">
                            <v-card-title class="d-flex flex-column align-items-center text-center">
                                <UserProfilePicture />
                                <v-spacer class="pa-2" />
                                <div>
                                    <div>{{ user?.email }}</div>
                                </div>
                            </v-card-title>
                            <!-- <v-card-actions>
                                <v-btn text @click="navigate('/profile')" >Edit Profile</v-btn>
                            </v-card-actions> -->
                            <v-list>
                                <v-list-item v-for=" item in menuItems" :key="item.icon" @click="navigate(item.link)"
                                    :to="item.link">
                                    <template v-slot:prepend>
                                        <v-icon>{{ item.icon }}</v-icon>
                                    </template>
                                    <v-list-item-title>{{ item.text }}</v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-card>

                    </v-menu>
                </v-list-item>
            </v-toolbar-items>


            <!-- <v-progress-linear active="isLoading" :indeterminate="true" class="ma-0" slot="extension" /> -->
        </v-app-bar>

        <!-- Mobile Drawer (visible only on small screens) -->
        <v-navigation-drawer v-model="drawer" absolute persistent location="top">
            <v-list>
                <!-- List Items with Icon and Title -->
                <v-list-item v-for="(item, i) in menuItems" :key="i" @click="navigate(item.link)" color="primary"
                    :active="isActiveRoute(item.link)">
                    <template v-slot:prepend>
                        <v-icon :icon="item.icon"></v-icon>
                    </template>
                    <v-list-item-title>{{ item.text }}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
    </div>
</template>

<script>
import { defineComponent, ref, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useDisplay } from 'vuetify'; // Use Vuetify display helper
import UserProfilePicture from '@/components/UserProfilePicture.vue';

export default defineComponent({
    name: 'NavBarComponent',
    components: {
        UserProfilePicture,
    },
    data() {
        const router = useRouter();
        const { smAndDown } = useDisplay();
        const store = useAuthStore();

        return {
            isLoading: false,
            drawer: false,
            menuVisible: false,
            menuItems: [
                { text: 'Dashboard', icon: 'mdi-view-dashboard', link: '/dashboard' },
                { text: 'Users', icon: 'mdi-account-group', link: '/users' },
                { text: 'Wordle', icon: 'mdi-alpha-w-box-outline', link: '/wordle' },
                { text: 'Dictionary', icon: 'mdi-book-open-page-variant', link: '/words' },
                { text: 'Edit Profile', icon: 'mdi-account', link: '/profile' },
                { text: 'Logout', icon: 'mdi-logout', link: '/logout' },
            ],
            smAndDown,
            store,
            router,
        };
    },
    computed: {
        user() {
            return this.store.user;
        },
        drawerState() {
            return this.smAndDown ? this.drawer : false;
        },
    },
    watch: {
        'store.apiRequestLoading'(newVal) {
            this.isLoading = newVal;
        },
    },
    methods: {
        toggleDrawer() {
            if (this.smAndDown) {
                this.drawer = !this.drawer;
            }
        },
        navigate(link) {
            this.router.push(link);
            this.drawer = false;
            this.menuVisible = false;
        },
        isActiveRoute(link) {
            return true;
        },
    },
});
</script>

<style scoped>
/* Optional: Custom styles */
</style>
