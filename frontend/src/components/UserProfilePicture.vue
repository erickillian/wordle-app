<template>
    <v-dialog v-model="showImageDialog" max-width="1000px">
        <v-card>
            <v-card-title>Select Profile Picture</v-card-title>
            <v-card-text>
                <v-row>
                    <v-col v-for="(image, index) in imageOptions" :key="index" cols="12" sm="6" md="4" lg="3">
                        <v-hover v-slot="{ isHovering, props }">
                            <v-img :src="'/static/profile_pictures/' + image" width="128" height="128" v-bind="props"
                                class="mx-auto">
                                <v-btn icon @click="changeUserProfilePicture(image)" v-if="isHovering"
                                    style="opacity: 0.5; border-radius: 50%; width: 100%; height: 100%;"
                                    color="primary">
                                    <v-icon color="white" style="opacity: 1;">mdi-check</v-icon>
                                </v-btn>
                            </v-img>
                        </v-hover>
                    </v-col>
                </v-row>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="showImageDialog = false">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <v-hover v-slot:default="{ isHovering, props }">
        <v-badge class="d-flex justify-center custom-badge" location="bottom end" color="primary" offset-x="20"
            offset-y="20">
            <v-img :src="user.profile_picture" width="128" height="128" v-bind="props">
                <v-btn icon @click="showImageDialog = true" v-if="isHovering" size="128" style="opacity: 0.5;"
                    color="primary" class="d-flex align-center justify-center fill-height fill-width">
                    <v-icon color="white" style="opacity: 1;">mdi-pencil</v-icon>
                </v-btn>
            </v-img>
            <template v-slot:badge>
                <v-icon size="x-large">mdi-pencil</v-icon>
            </template>
        </v-badge>
    </v-hover>
</template>

<script>
import { defineComponent } from 'vue';
import { useAuthStore } from '@/stores/auth';

export default defineComponent({
    name: 'UserProfilePictureComponent',
    data() {
        return {
            showImageDialog: false,
            imageOptions: [
                "bat.png",
                "bear.png",
                "beaver.png",
                "buffalo.png",
                "camel.png",
                "cat.png",
                "chameleon.png",
                "cheetah.png",
                "cow.png",
                "deer.png",
                "dog.png",
                "duck.png",
                "eagle.png",
                "elephant.png",
                "fox.png",
                "frog.png",
                "giraffe.png",
                "goat.png",
                "gorilla.png",
                "hamster.png",
                "hen.png",
                "hippo.png",
                "horse.png",
                "kangaroo.png",
                "koala.png",
                "lemur.png",
                "lion.png",
                "llama.png",
                "monkey.png",
                "ostrich.png",
                "owl.png",
                "panda-bear.png",
                "penguin.png",
                "pig.png",
                "polar-bear.png",
                "rabbit.png",
                "raccoon.png",
                "rhinoceros.png",
                "shark.png",
                "sheep.png",
                "sloth.png",
                "snake.png",
                "squirrel.png",
                "swan.png",
                "tiger.png",
                "turtle.png",
                "walrus.png",
                "wild-boar.png",
                "wolf.png",
                "zebra.png"
            ],
        };
    },
    computed: {
        user() {
            const store = useAuthStore();
            return store.user;
        },
    },
    methods: {
        async changeUserProfilePicture(image) {
            const authStore = useAuthStore();
            await authStore.editUserInfo({ profile_picture: image });
            this.user = authStore.user;
            this.$toast.success('User Profile Picture updated successfully');
            this.showImageDialog = false;
        },
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
