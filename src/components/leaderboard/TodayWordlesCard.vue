<template>
    <v-card>
        <v-subheader>
        <v-icon left>mdi-trophy</v-icon>
        {{ title }}
        </v-subheader>
        <v-data-table
            :headers="headers"
            :items=wordles
            :items-per-page="-1"
            class="elevation-1"
            hide-default-footer
            @click:row="playerClick"
        >
            <template v-slot:[`item.player_name`]="{ index, item }">
                <v-list-item-title>
                    <v-icon
                        dense
                        v-if="index + 1 <= 3"
                        :class="$store.state.placeClasses[index + 1]"
                    >
                        mdi-star-circle
                    </v-icon>
                    {{ item.player_name }}
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
  data () {
      return {
        headers: [
          {
            text: 'Player',
            align: 'start',
            sortable: false,
            value: 'player_name',
          },
          { text: 'Guesses', sortable: false, value: 'guesses' },
          { 
            text: 'Word',
            value: 'word',
            sortable: false,
          },
          { text: 'Time', sortable: false, value: 'time' },
        ],
      }
    },
  props: {
    title: String,
    wordles: Array,
  },
  methods: {
    playerClick(row) {
      this.wordles.map((wordle) => {
        if (wordle == row) {
          let url = `/players/${wordle.player}`
          this.$router.push(url)
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
