<template>
    <v-sheet elevation="0" class="mx-auto" color="transparent" max-width="1600">
        <v-row>
            <v-col cols="12" md="5" lg="3">
                <v-card>
                    <v-card-text class="d-flex flex-column align-items-center pa-10">
                        <UserProfilePicture />

                        <div class="text-center mt-5">
                            <h3 class="text-h6 font-weight-bold">
                                {{ user.display_name }}
                            </h3>
                            <p class="text-body-2">{{ user.about }}</p>
                        </div>
                    </v-card-text>

                    <v-divider></v-divider>
                    <div class="py-5 px-10">
                        <v-icon color="grey"> mdi-email-check-outline </v-icon>
                        <span class="ml-4">{{ user.email }}</span>
                    </div>
                    <v-divider></v-divider>
                    <div class="py-5 px-10">
                        <v-icon color="grey"> mdi-calendar </v-icon>
                        <span class="ml-4">{{ new Date(user.date_joined).toLocaleString() }}</span>
                    </div>
                </v-card>
            </v-col>
            <v-col cols="12" md="7" lg="9">
                <!-- Basic Information -->
                <v-card class="mb-5">
                    <v-card-title class="py-4 font-weight-bold">
                        Basic Information
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="pa-7">
                        <v-row>
                            <v-col cols="12" sm="6" v-for="user_property in user_properties">
                                <v-label class="font-weight-medium mb-2">{{user_property.name}}</v-label>
                                <v-text-field v-model="editUser[user_property.value]" color="primary" variant="outlined"
                                    density="compact" :type="user_property.value === 'email' ? 'email' : 'text'"
                                    :placeholder="user_property.name" :readonly="!user_property.is_editable"
                                    hide-details :disabled="!user_property.is_editable"
                                    :maxlength="user_property.max_length || null" />
                            </v-col>
                        </v-row>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions class="pa-5">
                        <v-spacer></v-spacer>
                        <v-btn class="px-5" color="primary" elevation="1" variant="elevated" @click="saveChanges()">
                            Update Basic Info
                        </v-btn>
                    </v-card-actions>
                </v-card>

                <!-- Appearance -->
                <v-card class="mb-5">
                    <v-card-title class="py-4 font-weight-bold">
                        Appearance
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="pa-7">
                        <v-card-actions>
                            <v-btn-toggle rounded="pill" v-model="user.color_mode" @update:modelValue="updateColorMode"
                                mandatory>
                                <v-btn v-for="option in color_mode_options" :key="option.value" :value="option.value">
                                    <v-icon left>{{ option.icon }}</v-icon>
                                    {{ option.name }}
                                </v-btn>
                            </v-btn-toggle>
                        </v-card-actions>
                    </v-card-text>
                </v-card>
                <UserSessionCard />
            </v-col>
        </v-row>
        <v-snackbar v-model="showSnackbar" :timeout="3000" color="success">
            {{ snackbarMessage }}
        </v-snackbar>
    </v-sheet>
</template>

<script>
import { defineComponent, ref, watch, computed, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useTheme } from 'vuetify';
import { getUserSessions } from '@/api/auth';
import UserSessionCard from '@/components/UserSessionCard.vue';
import UserProfilePicture from '@/components/UserProfilePicture.vue';

export default defineComponent({
    name: 'UserSelfComponent',  
    components: {
        UserSessionCard,
        UserProfilePicture,
    },
    data() {
        return {
            activeTab: 'userInfo',
            user_properties: [
                { name: 'Full Name', value: 'full_name', is_editable: true, max_length: 50 },
                { name: 'Email', value: 'email', is_editable: false },
            ],
            color_mode_options: [
                { name: 'Light', value: 'light', icon: 'mdi-weather-sunny' },
                { name: 'Dark', value: 'dark', icon: 'mdi-moon-waning-crescent' },
                { name: 'System', value: 'system', icon: 'mdi-desktop-classic' },
            ],
            tabs: [
                { label: 'User Info', value: 'userInfo', icon: 'mdi-account' },
                { label: 'Appearance', value: 'appearance', icon: 'mdi-palette' },
                { label: 'Security', value: 'security', icon: 'mdi-lock' },
            ],
        };
    },
    setup() {
        const authStore = useAuthStore();
        const theme = useTheme();

        // Reactive references
        const editing = ref({});
        const userLoading = ref(authStore.user_loading);
        const user = ref({ ...authStore.user });  // Makes a local copy of the user object
        const editUser = ref({ ...authStore.user });  // Makes a local copy of the user object for editing values
        const showImageDialog = ref(false);
        const showSnackbar = ref(false);
        const snackbarMessage = ref('');

        const userSessionsLoading = ref(false);
        const userSessions = ref([]);
        const userSessionsPage = ref({});

        const updateColorMode = async (colorMode) => {
            user.value.color_mode = colorMode;
            theme.global.name.value = colorMode;
            await authStore.editUserInfo({ color_mode: colorMode });
            user.value = { ...authStore.user };
            editUser.value = { ...authStore.user };
            showSnackbar.value = true;
            snackbarMessage.value = 'Color Mode updated successfully';
        };

        function toggleEdit(propertyName) {
            // Toggle edit mode for the specific property
            editing.value[propertyName] = !editing.value[propertyName];
        }

        async function saveChanges() {
            await authStore.editUserInfo(editUser.value);
            user.value = { ...authStore.user };
            editUser.value = { ...authStore.user };
            showSnackbar.value = true;
            snackbarMessage.value = 'User Profile updated successfully';
        }

        function cancelEdit(propertyName) {
            // Revert to the original value and exit edit mode
            user.value[propertyName] = originalUser.value[propertyName];
            editing.value[propertyName] = false;
        }

        function getProfilePictureUrl(picture_url) {
            return `/static/profile_pictures/${picture_url}`;
        }

        async function changeUserProfilePicture(image) {
            image = image.split('/').pop();
            await authStore.editUserInfo({ profile_picture: image });
            user.value.profile_picture = image;
            showImageDialog.value = false;
            showSnackbar.value = true;
            snackbarMessage.value = 'User Profile Picture updated successfully';
        }

        const profilePictureUrl = computed(() => {
            return getProfilePictureUrl(user.value.profile_picture);
        });

        function triggerImageDialog() {
            console.log("Dialog clicked !");
        }

        function handleFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                const formData = new FormData();
                formData.append('profile_picture', file);

                // Simulate an API call to upload the file
                // Replace this with your actual API call
                setTimeout(() => {
                    // Simulate a successful upload and update the profile picture URL
                    user.value.profile_picture = file.name;
                    authStore.editUserInfo({ profile_picture: file.name });
                }, 1000);
            }
        }

        async function fetchActiveTokens() {
            userSessionsLoading.value = true;
            try {
                const response = await getUserSessions();
                userSessions.value = response.data.results;
                userSessionsPage.value = response.data.page;
            } catch (error) {
                console.error('Error fetching active tokens:', error);
            } finally {
                userSessionsLoading.value = false;
            }
        }

        onMounted(() => {
            fetchActiveTokens();
        });

        return {
            editing,
            userLoading,
            toggleEdit,
            saveChanges,
            cancelEdit,
            updateColorMode,
            user,
            editUser,
            profilePictureUrl,
            triggerImageDialog,
            handleFileChange,
            getProfilePictureUrl,
            changeUserProfilePicture,
            showImageDialog,
            showSnackbar,
            snackbarMessage,

            userSessions,
        };
    },
});
</script>

<style lang="scss">
.custom-badge {
    .v-badge__badge {
        width: 30px;
        height: 30px;
        border-radius: 30px;
    }
}
</style>
