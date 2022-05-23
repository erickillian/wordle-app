<template>
    <WordleGame />
</template>

<script>
import axios from "axios";
import WordleGame from "../wordle/WordleGame";

export default {
  name: "home",
  components: { WordleGame},
  created() {
    this.$store.dispatch("fetchLeaderboard");
  },
};
</script>
