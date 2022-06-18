<template>
  <v-card style="height: 100%">
    <v-card-title>
      <div class="overline">{{ $t("player_card.name") }}</div>
    </v-card-title>
    <v-card-title class="py-0">
        <v-row>
          <v-col class="body-2 font-weight-light">
            <p class="headline mb-1">{{ playerStats.full_name }}</p>
            <span class="font-weight-bold"></span>
            {{ }}
            <br>
            <v-spacer></v-spacer>
          </v-col>
        </v-row>
      </v-card-title>
      <v-card-text>
      <v-row>
        <v-col style="overflow: auto">
          <v-tabs 
            color="blue lighten-1"
            :vertical="false"
            grow
          >
            <v-tab :title="$t('player_card.info.name')"><v-icon>mdi-chart-bubble</v-icon></v-tab>
            <v-tab title="Convergle Guess Distribution"><v-icon>mdi-chart-areaspline</v-icon></v-tab>
            <v-tab :title="$t('player_card.history.name')"><v-icon>mdi-file-chart-outline</v-icon></v-tab>

           <v-tab-item class="pa-2">
              <p class="overline">{{ $t('player_card.info.name') }}</p>
              <v-list disabled>
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
              <p class="overline">Convergle Guess Distribution</p>
              <BarChart
              :height="155"
              :chartData="chartData"
              :options="chartOptions"
              :key=guessDistribution.guesses
               />
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
                    :key=playerStats.id
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
import BarChart from "@/components/BarChart"
import WordleListCard from "@/components/leaderboard/WordleListCard"

export default {
  components: { BarChart, WordleListCard },
  props: {
    // playerInfo: Object,
    playerStats: Object,
    playerWordles: [],
    guessDistribution: Object,
    // ratingHistory: Array,
    // matchHistory: Array
  },
    created() {
        if (this.$route.params.id) {
            this.$store.dispatch('player/stats', this.$route.params.id);
            this.$store.dispatch('player/wordles', this.$route.params.id);
            this.$store.dispatch('player/guessDistribution', this.$route.params.id);
        }
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
            },
            animation: {
                duration: 0
            }
        },
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
    chartData() {
        return {
            labels: this.guessDistribution.labels,//.guess_distribution.labels,
            datasets: [ 
                { 
                    data: this.guessDistribution.data, //this.$store.player.guess_distribution.data ,
                    backgroundColor: 'hsl(212, 54%, 30%)',
                } 
            ]
        }
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