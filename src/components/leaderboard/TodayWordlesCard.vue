<template>
    <v-card>
        <v-subheader>
        <v-icon left>mdi-trophy</v-icon>
        {{ title }}
        </v-subheader>
        <v-data-table
          :headers="headers"
          :items=wordles
          :items-per-page="5"
          class="elevation-1"
          @click:row="playerClick"
        >
          <template v-slot:[`item.guesses`]="{ item }">
            <v-chip
              :color="getColor(item.fail)"
              dark
              @click="playerClick(item.player)"
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
          { text: 'Guesses', value: 'guesses' },
          { 
            text: 'Word',
            value: 'word',
            sortable: false,
          },
          { text: 'Time', value: 'time' },
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
