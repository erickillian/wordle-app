<template>
  <v-row class="ma-0">
    <v-col>
        <v-row class="mb-3">
            <v-col
                class="pt-0"
            >
                <BigNumberCard 
                    title="Total Wordles"
                    :loading="$store.state.wordle.stats_loading"
                    :value="$store.state.wordle.stats.num_wordles"
                    :key="$store.state.wordle.stats"
                />
            </v-col>
            <v-col
                class="pt-0"
            >
                <BigNumberCard 
                    title="Total Players"
                    :loading="$store.state.wordle.stats_loading"
                    :value="$store.state.wordle.stats.num_players"
                    :key="$store.state.wordle.stats"
                />
            </v-col>
        </v-row>

        <!--v-row class="mb-3">
            <v-col class="pt-0">
                <LeadersCard
                :title="$t('leaderboard.top')"
                :leaders="$store.state.lb.leaders"
                />
            </v-col>
        </v-row-->
        <v-row class="mb-3">
            <v-col class="pt-0">
                <WordleListCard
                    title="Todays Convergles"
                    icon="mdi-trophy"
                    :items="$store.state.leaderboards.wordle.today"
                    :headers="todays_wordle_headers"
                    :items_per_page="10"
                    :hide_footer="false"
                />
            </v-col>
        </v-row>
        
    </v-col>
    <v-col>
         <v-row class="mb-3">
            <v-col class="pt-0">
                <WordleListCard
                    title="Top Average Guesses"
                    icon="mdi-trophy"
                    :items="$store.state.leaderboards.wordle.leaders.avg_guesses"
                    :headers="avg_guesses_headers"
                    :items_per_page="5"
                    :hide_footer="true"
                />
            </v-col>
            <v-col class="pt-0">
                <WordleListCard
                    title="Top Average Time"
                    icon="mdi-trophy"
                    :items="$store.state.leaderboards.wordle.leaders.avg_time"
                    :headers="avg_time_headers"
                    :items_per_page="5"
                    :hide_footer="true"
                />
            </v-col>
        </v-row>
        <v-row class="mb-3">
            <v-col class="pt-0">
                <WordleListCard
                    title="Convergle Wall of Shame"
                    icon="mdi-alert-outline"
                    :items="$store.state.leaderboards.wordle.shame"
                    :headers="wall_of_shame_headers"
                    :items_per_page="-1"
                    :hide_footer="true"
                />
            </v-col>
        </v-row>
      <!--SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.most_games')"
        :content="$store.state.lb.maxes.games"
        valueClass="green--text text--accent-4"
        cardClass="mb-3"
      /-->

      <!--SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.winrate')"
        :content="$store.state.lb.maxes.winrate"
        valueFilter="percent"
        valueClass="green--text text--accent-4"
        cardClass="mb-3"
      /-->

      <!--SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.effective')"
        :content="$store.state.lb.maxes.efficiency"
        valueClass="green--text text--accent-4"
      /-->
    </v-col>
    <!-- <v-col>
      <SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.rise')"
        :content="$store.state.lb.weekly.best"
        valueClass="green--text text--accent-4"
        cardClass="mb-3"
        dense
      />
      <SimpleCard
        icon="mdi-thumb-down"
        :title="$t('leaderboard.fall')"
        :content="$store.state.lb.weekly.worst"
        valueClass="red--text text--accent-4"
        dense
      />
    </v-col> -->
  </v-row>
</template>

<script>
import axios from "axios";
// import SimpleCard from "../components/leaderboard/SimpleCard";
// import LeadersCard from "../components/leaderboard/LeadersCard";
import BigNumberCard from "@/components/leaderboard/BigNumberCard";
import WordleListCard from "@/components/leaderboard/WordleListCard";

export default {
    name: "HomeView",
    components: { BigNumberCard, WordleListCard },
    created() {
        this.$store.dispatch("wordle/stats");
        this.$store.dispatch("leaderboards/wordleFails");
        this.$store.dispatch("leaderboards/todaysWordles");
        this.$store.dispatch("leaderboards/wordleAvgGuesses");
        this.$store.dispatch("leaderboards/wordleAvgTime");
    },
    data () {
        return {
            todays_wordle_headers: [
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
                { text: 'Streak', sortable: false, value: 'streak' },
            ],
            wall_of_shame_headers: [
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
            avg_guesses_headers: [
                {
                    text: 'Player',
                    align: 'start',
                    sortable: false,
                    value: 'full_name',
                },
                {
                    text: 'Average Guesses',
                    sortable: false,
                    value: 'avg_guesses',
                },
            ],
            avg_time_headers: [
                {
                    text: 'Player',
                    align: 'start',
                    sortable: false,
                    value: 'full_name',
                },
                {
                    text: 'Average Time',
                    sortable: false,
                    value: 'avg_time',
                },
            ],
        }
    },
};
</script>
