<template>
    <v-card>
        <v-subheader>
        <v-icon left color=red>mdi-alert-outline</v-icon>
        {{ title }}
        <v-spacer/>
        </v-subheader>
        <v-data-table
          :headers="headers"
          :items=wordleFails
          class="elevation-1"
          @click:row="playerClick"
          hide-default-footer
        :items-per-page="all"
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
        search: '',
        headers: [
          {
            text: 'Player',
            align: 'start',
            sortable: false,
            value: 'player_name',
          },
          { 
            text: 'Word',
            value: 'word',
            sortable: false,
          },
          {
            text: 'Date',
            sortable: false,
            value: 'date',
          },
        ],
      }
    },
  props: {
    title: String,
    wordleFails: Array,
  },
  methods: {
    playerClick(row) {
      this.wordleFails.map((wordle) => {
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
