<template>
    <WordleGame />
</template>

<script>
import axios from "axios";
import WordleGame from "../wordle/WordleGame";

export default {
  name: "WordleView",
  components: { WordleGame},
  created() {
    this.$store.dispatch("fetchLeaderboard");
  },
};
</script>
