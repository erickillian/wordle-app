<template>
    <v-card>
        <v-subheader>
            <v-icon left> {{ icon }}</v-icon>
            {{ title }}
        </v-subheader>
        <v-data-table
            :headers="headers"
            :items="items"
            :items-per-page="items_per_page"
            class="elevation-1"
            @click:row="playerClick"
            v-bind:hide-default-footer="hide_footer"
        >
            <template v-slot:[`item.player_name`]="{ item }">
                <v-list-item-title>
                    <v-icon
                        dense
                        v-if="item.rank <= 3"
                        :class="$store.state.placeClasses[item.rank]"
                    >
                        mdi-star-circle
                    </v-icon>
                    {{ item.player_name }}
                </v-list-item-title>
            </template>
            <template v-slot:[`item.full_name`]="{ index, item }">
                <v-list-item-title>
                    <v-icon
                        dense
                        v-if="index + 1 <= 3"
                        :class="$store.state.placeClasses[index + 1]"
                    >
                        mdi-star-circle
                    </v-icon>
                    {{ item.full_name }}
                </v-list-item-title>
            </template>
            <template v-slot:[`item.guesses`]="{ item }">
                <v-chip
                :color="getColor(item.fail)"
                >
                {{ item.guesses }}
                </v-chip>
            </template>
        </v-data-table>
    </v-card>
</template>

<script>

export default {
  
  props: {
    title: String,
    icon: String,
    items: Array,
    headers: Array,
    items_per_page: Number,
    hide_footer: Boolean,
  },
  methods: {
    playerClick(row) {
        this.items.map((item) => {
            if (item == row) {
                if (item.player) {
                    this.$router.push(`/players/${item.player}`)
                } else if (item.id) {
                    this.$router.push(`/players/${item.id}`)
                }
            }
        })
    },
    getColor (fail) {
        if (fail) return 'red'
        else return 'green'
    },
  },
}

</script>
