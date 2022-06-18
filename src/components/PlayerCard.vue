<template>
  <v-card style="height: 100%">
    <v-card-title>
      <div class="overline">{{ $t("player_card.name") }}</div>
    </v-card-title>
    <!-- <v-card-title class="py-0">
        <v-row>
          <v-col cols="4" md="2" class="text-center" justify="center">
            <v-avatar size="60">
              <img
                src="https://eitrawmaterials.eu/wp-content/uploads/2016/09/empty-avatar.jpg"
              >
            </v-avatar>
            <br>
            <div :title="`${$t('player_card.rating')} ${playerInfo.rating}`">
              <v-icon class="red--text text--lighten-1">mdi-star-circle-outline</v-icon>
              <span
              style="vertical-align:middle"
              class="font-weight-bold blue--text subtitle-2">
                {{ playerInfo.rating }}
              </span>
            </div>
          </v-col>
          <v-col class="body-2 font-weight-light">
            <p class="headline mb-1">{{ fullname }}</p>
            <span class="font-weight-bold">{{ $t("player_card.city") }}:</span>
            {{ playerInfo.city }}
            <br>
            <v-spacer></v-spacer>
            <span class="font-weight-bold">{{ $t("player_card.date_of_birth") }}:</span>
            {{ playerInfo.date_of_birth | date }}
          </v-col>
        </v-row>
      </v-card-title> -->
      <v-card-text>
      <v-row>
        <v-col style="overflow: auto">
          <v-tabs 
            color="blue lighten-1"
            :vertical="false"
            grow
          >
            <v-tab :title="$t('player_card.info.name')"><v-icon>mdi-chart-bubble</v-icon></v-tab>
            <v-tab :title="$t('player_card.chart.name')"><v-icon>mdi-chart-areaspline</v-icon></v-tab>
            <v-tab :title="$t('player_card.history.name')"><v-icon>mdi-file-chart-outline</v-icon></v-tab>

           <v-tab-item class="pa-2">
              <p class="overline">{{ $t('player_card.info.name') }}</p>
              <v-list disabled v-if="playerStats">
                <v-list-item-group>
                  <v-list-item
                    v-for="(item, index) in statItems"
                    :key="index"
                  >
                    <v-list-item-icon>
                      <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ item.title }}</v-list-item-title>
                      <v-list-item-subtitle>{{ item.subtitle }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-tab-item>

            <v-tab-item class="pa-2">
              <p class="overline">{{ $t('player_card.chart.name') }}</p>
              <line-chart
              :height="155"
              :chartData={}
              :options="chartOptions" />
            </v-tab-item>

            <v-tab-item class="pa-2">
              <p class="overline">{{ $t('player_card.history.name') }}</p>
              <WordleListCard
                    title="Convergle History"
                    icon="mdi-history"
                    :items="playerWordles"
                    :headers="todays_wordle_headers"
                    :items_per_page="10"
                    :hide_footer="false"
                />
                <!-- <template v-slot:item.event_date="{ item }">
                  {{ item.event_date | date}}
                </template>
                <template v-slot:item.score="{ item }">
                  <b>{{ item.score }}</b>
                </template>
                <template v-slot:item.delta="{ item }">
                  <span :class="getDeltaClass(item)">{{ getDeltaValue(item) }}</span>
                </template> -->
            </v-tab-item>
          </v-tabs>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import LineChart from "@/components/LineChart"
import WordleListCard from "@/components/leaderboard/WordleListCard"

export default {
  components: { LineChart, WordleListCard },
  props: {
    // playerInfo: Object,
    playerStats: Object,
    playerWordles: Array,
    // ratingHistory: Array,
    // matchHistory: Array
  },
  data() {
    return {
        todays_wordle_headers: [
            { 
                text: 'Word',
                value: 'word',
                sortable: true,
            },
            { text: 'Guesses', sortable: true, value: 'guesses' },
            { text: 'Time', sortable: true, value: 'time' },
            { text: 'Date', sortable: true, value: 'date' },
        ],
        chartOptions: {
            legend: {
                display: false
            }
        }
    }
  },
  methods: {
    getDeltaClass(item) {
      if (item.result) {
        return 'green--text text--accent-4 font-weight-bold'
      } else {
        return 'red--text text--accent-4 font-weight-bold'
      }
    },
    getDeltaValue(item) {
      if (item.result) {
        return item.delta
      } else {
        return item.delta * -1
      }
    }
  },
  computed: {
    fullname () {
      return `${this.playerStats.first_name} ${this.playerStats.last_name}`
    },
    statItems () {
      return [
        {
          icon: "mdi-account-outline",
          title: this.$t('player_card.info.fullname'),
          subtitle: this.playerStats.full_name
        },
        { 
          icon: "mdi-chart-donut",
          title: `${this.$t('player_card.info.total_wordles')}: ${this.playerStats.total_wordles}`,
          subtitle: `${this.$options.filters.percent((this.playerStats.total_wordles - this.playerStats.fails) / this.playerStats.total_wordles, 2)} Solved`
        },
        {
          icon: "mdi-star",
          title: `${this.$t('player_card.info.avg_guesses')}: ${this.$options.filters.round(
            this.playerStats.avg_guesses, 2
          )}`,
        },
        {
          icon: "mdi-summit",
          title: `${this.$t('player_card.info.avg_time')}: ${this.playerStats.avg_time}`,
        },
      ]

    },
  }
};
</script>

<style>
  .v-data-table table tr td {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
</style>
