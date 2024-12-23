<template>
    <v-card max-width="400">
        <v-card-title style="text-align: center; display: flex; flex-direction: column; align-items: center;">
            <v-img v-if="wordle?.user?.profile_picture" :src="wordle.user.profile_picture" alt="Profile Picture" width="64" height="64" />
            <div>{{ wordle?.user?.display_name ? wordle.user.display_name : 'Unknown User' }}</div>
        </v-card-title>
        <v-card-subtitle style="margin-bottom: 10px;">
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <div style="display: flex; justify-content: space-between;">
                    <span v-if="wordle.start_time">Daily Rank ({{ formatDate(wordle.start_time) }}):</span>
                    <span v-else>Daily Rank:</span>
                    <span>
                        <span v-if="wordle.daily_rank === 1"><strong>🥇 1st</strong></span>
                        <span v-else-if="wordle.daily_rank === 2"><strong>🥈 2nd</strong></span>
                        <span v-else-if="wordle.daily_rank === 3"><strong>🥉 3rd</strong></span>
                        <span v-else><strong>{{ formatRank(wordle.daily_rank) }}</strong></span>
                    </span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Word Rank ({{ wordle.word ? wordle.word : 'N/A' }}):</span>
                    <span>
                        <span v-if="wordle.word_rank === 1"><strong>🥇 1st</strong></span>
                        <span v-else-if="wordle.word_rank === 2"><strong>🥈 2nd</strong></span>
                        <span v-else-if="wordle.word_rank === 3"><strong>🥉 3rd</strong></span>
                        <span v-else><strong>{{ formatRank(wordle.word_rank) }}</strong></span>
                    </span>
                </div>
            </div>
        </v-card-subtitle>
    </v-card>
</template>

<script>
export default {
    name: 'ExtraWordleRankingsCard',
    props: {
        wordle: {
            type: Object,
        },
    },
    methods: {
        formatRank(rank) {
            if (!rank) return 'N/A';
            const suffixes = ['th', 'st', 'nd', 'rd'];
            const v = rank % 100;
            return rank + (suffixes[(v - 20) % 10] || suffixes[v] || suffixes[0]);
        },
        formatDate(dateString) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        },
    },
};
</script>

<style scoped>

</style>