<template>
  <v-app-bar
    dense
    app
    extended
    extension-height="0"
    :elevation="2"
    :clipped-left="true"
  >
    <img
      style="max-width: 40px; max-height: 40px"
      class="mr-3"
      src="/static/logo.png"
    />
    <v-toolbar-title>Converge General Sports Ranker</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-toolbar-items class="hidden-sm-and-down">
      <v-btn text v-for="item in menu"
        :key="item.icon"
        :to="item.to"
        :href="item.href"
        :target="item.target"
      >
        <v-icon :left="true">{{ item.icon }}</v-icon>
        {{ item.name }}
      </v-btn>
    </v-toolbar-items>
    <div class="hidden-md-and-up">
      <v-menu>
        <template v-slot:activator="{ on }">
          <v-btn text v-on="on">
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item v-for="item in menu" :key="item.icon">
            <v-btn text 
              :to="item.to"
              :href="item.href"
              :target="item.target"
            >
              <v-icon :left="true">{{ item.icon }}</v-icon>
              {{ item.name }}
            </v-btn>
          </v-list-item>   
        </v-list>
      </v-menu>
    </div>
    <v-progress-linear
      :active="$store.state.isLoading"
      :indeterminate="true"
      class="ma-0"
      slot="extension" />
  </v-app-bar>
</template>

<script>
export default {
  data() {
    return {
      menu: [
        {name: this.$t("nav.main"), icon: "mdi-home-outline", to: "/"},
        {name: this.$t("nav.players"), icon: "mdi-account", to: "/players"},
        // {name: this.$t("nav.events"), icon: "mdi-bank", to: "/events"},
      ]
    }
  }
};
</script>

<style scoped>
  a {
    text-decoration: none;
  }
</style>
