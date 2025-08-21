<template>
    <v-card>
        <v-card-text>
            <p class="text-h6">
                <v-icon left class="mr-2">{{ icon }}</v-icon>
                {{ title }}
            </p>

            <!-- Info Button -->
            <div style="position: absolute; top: 10px; right: 10px;">
                <v-btn icon @click="dialog = true" elevation="0">
                    <v-icon>mdi-information-outline</v-icon>
                </v-btn>
            </div>

            <!-- Info Dialog -->
            <v-dialog v-model="dialog" max-width="600px">
                <v-card>
                    <v-card-title>
                        <span class="text-h6">{{ title }}</span>
                    </v-card-title>
                    <v-card-text>
                        <slot></slot>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="primary" text @click="dialog = false">Close</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-card-text>

        <v-data-table-server :headers="computedHeaders" :items="items" class="elevation-0" hide-default-footer
            disable-sort hover @click:row="handleRowClick" :items-length="items.length" :loading="loading">

            <!-- Pagination -->
            <template v-slot:bottom>
                <div class="d-flex justify-center py-4 align-center" v-if="page ? page.total_pages > 1 : false">
                    <v-pagination v-model="page.current_page" :length="page ? page.total_pages : 0"
                        :total-visible="numPagination" size="small" aria-label="Pagination"
                        @update:model-value="onPageUpdate"></v-pagination>
                </div>
            </template>

            <!-- No Data -->
            <template v-slot:no-data>
                <div class="pa-4">
                    <v-alert :value="true" icon="mdi-information">
                        No data found.
                    </v-alert>
                </div>
            </template>

            <template v-slot:["item"]="{ item, index }">
                <tr v-ripple @click="handleRowClick(item)" style="cursor: pointer;">
                    <!-- Iterate over headers dynamically -->
                    <template v-for="(header, key) in computedHeaders" :key="key">
                        <td>
                            <!-- Check if a custom slot is defined for the column -->
                            <template v-if="header.key == 'rank'">
                                <v-list-item-title>
                                    <v-icon v-if="item.rank <= 3"
                                        :color="placeColors[item.rank]">
                                        mdi-star-circle
                                    </v-icon>
                                    {{ item.rank}}
                                </v-list-item-title>
                            </template>
                            <template v-if="header.key == 'user'">
                                <div style="display: flex; align-items: center;">
                                    <v-list-item-media>
                                        <v-img
                                            :src="item.user ? item.user.profile_picture : getProfilePictureUrl(item.profile_picture)"
                                            width="32" height="32" class="mr-2" />
                                    </v-list-item-media>

                                    <v-list-item-title>
                                        {{ item.user ? (item.user.display_name) : (item.display_name) }}
                                    </v-list-item-title>
                                </div>
                            </template>
                            <template v-else-if="header.key == 'guesses'">
                                <v-chip :color="getColor(item.solved)">
                                    {{ item.guesses }}
                                </v-chip>
                            </template>
                            <template v-else-if="header.key == 'start_time'">
                                <v-list-item-title>
                                    {{ new Date(item.start_time).toLocaleDateString('en-US', { timeZone: 'UTC', year:
                                    'numeric', month: 'long', day: 'numeric' }) }}
                                </v-list-item-title>
                            </template>

                            <template v-else>
                                <!-- Default handling if no custom slot exists -->
                                <span v-if="header.key === 'rank'">
                                    <slot :name="`item.rank`" :item="item" :index="index"></slot>
                                </span>
                                <span v-else>
                                    {{ item[header.key] }}
                                </span>
                            </template>
                        </td>
                    </template>
                </tr>
            </template>
        </v-data-table-server>
    </v-card>
</template>

<script lang>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

export default {
    props: {
        title: String,
        icon: String,
        items: Array,
        headers: Array,
        hide_footer: {
            type: Boolean,
            default: true
        },
        page: {
            type: Object,
            required: false,
            default: () => ({
                current_page: 1,
                page_size: 10,
                total_pages: 1,
                has_next: false,
                has_prev: false,
            }),
        },
        pageChange: {
            type: Function,
            required: false,
        },
        loading: {
            type: Boolean,
            default: false,
            required: false,
        },
        rankItems: {
            type: Boolean,
            default: false,
            required: false,
        },
        numPagination: {
            type: Number,
            default: 5,
            required: false,
        },
    },
    data() {
        return {
            dialog: false,  // State to control the dialog visibility
            placeColors: {
                1: "amber darken-3", // Gold
                2: "blue-grey lighten-5", // Silver
                3: "brown darken-2", // Bronze
            },
        };
    },
    setup(props) {
        const router = useRouter();

        const placeClasses = {
            1: "yellow--text text--accent-4",
            2: "blue-grey--text text--lighten-4",
            3: "brown--text text--darken-1",
        };

        const handleRowClick = (item, event) => {
            if (item.user) {  // wordles have the user attribute but users do not as they are the user
                router.push(`/wordle/${item.slug}`);
            } else {
                router.push(`/users/${item.slug}`);
            }
        }

        const getColor = (solved) => {
            return solved ? "green" : "red";
        };

        const computedHeaders = computed(() => {
            let headers = [...props.headers];
            if (props.rankItems) {
                headers.unshift({
                    align: 'start',
                    key: 'rank',
                    title: 'Rank'
                });
            }
            return headers;
        });

        function getProfilePictureUrl(picture_url) {
            return `/static/profile_pictures/${picture_url}`;
        }

        const onPageUpdate = (newPage) => {
            props.pageChange(newPage);
        };

        return {
            handleRowClick,
            getColor,
            computedHeaders,
            onPageUpdate,
            getProfilePictureUrl,
        };
    },
};
</script>

<style scoped></style>
