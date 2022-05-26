<template>
    <v-card>
        <v-subheader>
        <v-icon left>mdi-trophy</v-icon>
        {{ title }}
        </v-subheader>
        <v-list flat dense>
            <v-list-item-group>
        <v-row
          dense
          align="center"
          justify="center"
          v-for="(wordle) in wordles"
          :key="wordle.id"
          @click="playerClick(wordle.player)"
        >
          <v-col>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>
                  {{ wordle.player_name }}
                </v-list-item-title>
              </v-list-item-content>
              <v-list-item-content>
                <v-list-item-title>
                  {{ wordle.guesses }}
                </v-list-item-title>
              </v-list-item-content>
              <v-list-item-content>
                <v-list-item-title>
                  {{ wordle.word }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
      </v-list-item-group>
        </v-list>
    </v-card>
</template>

<script>

export default {
  props: {
    title: String,
    wordles: Array,
  },
  methods: {
    playerClick(player_id) {
      let url = `/players/${player_id}`
      this.$router.push(url)
    }
  },
}

</script>
