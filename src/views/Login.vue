<template>
   <v-app id="login-view">
      <v-main>
         <v-container fluid fill-height>
            <v-layout align-center justify-center>
               <v-flex xs12 sm8 md4>
                  <v-card class="elevation-12">
                     <v-toolbar dark color="primary">
                        <v-toolbar-title>Login</v-toolbar-title>
                     </v-toolbar>
                     <v-card-text>
                        <v-form @submit.prevent="submit">
                           <v-text-field
                              prepend-icon=mdi-account
                              name="login"
                              label="Login"
                              type="username"
                              placeholder="username"
                              v-model="inputs.username"
                              :error-messages="$store.state.auth.login_error.username"
                           ></v-text-field>
                           <v-text-field
                              id="password"
                              prepend-icon=mdi-lock
                              name="password"
                              label="Password"
                              type="password"
                              placeholder="password"
                              v-model="inputs.password"
                              :error-messages="$store.state.auth.login_error.password"
                           ></v-text-field>
                           <v-btn
                              type="submit"
                              color="primary"
                              class="mr-4"
                              @click="login(inputs)"
                              @submit="login(inputs)"
                              :loading=$store.state.auth.authenticating
                            >
                              Login
                            </v-btn>
                        </v-form>
                     </v-card-text>
                     <!-- <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn @submit="login(inputs)" @click="login(inputs)" color="primary" to="/">Login</v-btn>
                     </v-card-actions> -->
                      <router-link to="/register">create account</router-link> |
                      <router-link to="/password_reset">reset password</router-link>
                  </v-card>
               </v-flex>
            </v-layout>
         </v-container>
      </v-main>
   </v-app>
</template>

<script>
export default {
  data() {
    return {
      inputs: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    login({ username, password }) {
      this.$store.dispatch('auth/login', { username, password })
        .then(() => this.$router.push('/'));
    },
  },
};
</script>

<style>
form input {
  display: block

}
</style>