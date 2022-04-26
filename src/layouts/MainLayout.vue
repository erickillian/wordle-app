<template>
  <v-app id="app">
    <navbar />
    <v-main>
      <v-container fill-height fluid>
          <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Navbar from "@/components/Navbar";

export default {
  name: "main-layout",
  components: { Navbar },
  data() {
    return {

    }
  }
};
</script>
