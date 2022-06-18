<template>
  <v-row dense class="mx-0" style="height: 100%">
    <v-navigation-drawer app :clipped="true" width="400" v-model="showSider">
      <player-list @player-clicked="onPlayerClick"/>
    </v-navigation-drawer>
    <v-col> 
        <v-card-text
            align-center
            v-if="$store.state.player.not_found"
        >
            <v-icon left class="red--text text--accent-2">
                mdi-alert-circle-outline
            </v-icon>
            <span class="red--text text--accent-2">
                {{ $t("player_card.notFound") }}
            </span>
        </v-card-text>
        <player-card
            v-else
            :playerStats="$store.state.player.stats"
            :playerWordles="$store.state.player.wordles"
        />
        <v-card>
            <v-card-title primary-title align-center>
                <v-icon left>
                mdi-arrow-left-circle-outline
                </v-icon>
                <span>{{ $t("player_card.placeholder") }}</span>
            </v-card-title>
        </v-card>
    </v-col>
      <v-btn
        fab
        small
        fixed
        right
        bottom
        dark
        color="red"
        @click.stop="showSider = !showSider"
      > 
        <v-icon v-if="showSider">mdi-arrow-left</v-icon>
        <v-icon v-else>mdi-account-circle</v-icon>
      </v-btn>
  </v-row>
</template>

<script>
import PlayerList from "../components/PlayerList"
import PlayerCard from "../components/PlayerCard"

export default {
  name: "PlayersView",
  components: { PlayerCard, PlayerList },
  data() {
    return {
      showSider: true
    }
  },
  methods: {
    onPlayerClick(player_id) {
      this.$router.push(`/players/${player_id}`).catch(err => {})
    }
  },
  watch: {
  },
}
</script>
