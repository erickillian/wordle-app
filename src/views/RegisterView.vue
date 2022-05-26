<!--template>
  <div id="register-view">
    <h1>Create Account</h1>
    <template v-if="registrationLoading">
      loading...
    </template>
    <template v-else-if="!registrationCompleted">
      <form @submit.prevent="submit">
        <input v-model="inputs.username" type="text" id="username" placeholder="username">
        <input v-model="inputs.password1" type="password" id="password1" placeholder="password">
        <input v-model="inputs.password2" type="password" id="password2"
          placeholder="confirm password">
        <input v-model="inputs.email" type="email" id="email" placeholder="email">
      </form>
      <button @click="createAccount(inputs)">
        create account
      </button>
      <span class="error" v-show="registrationError">
        An error occured while processing your request.
      </span>
      <div>
        Already have an account?
        <router-link to="/login">login</router-link> |
        <router-link to="/password_reset">reset password</router-link>
      </div>
    </template>
    <template v-else>
      <div>
        Registration complete. You should receive an email shortly with instructions on how to
        activate your account.
      </div>
      <div>
        <router-link to="/login">return to login page</router-link>
      </div>
    </template>
  </div>
</template-->
<template>
   <v-app id="login-view">
      <v-main>
         <v-container fluid fill-height>
            <v-layout align-center justify-center>
               <v-flex xs12 sm8 md4>
                  <v-card class="elevation-12">
                     <v-toolbar dark color="primary">
                        <v-toolbar-title>Create Account</v-toolbar-title>
                     </v-toolbar>
                     <v-card-text>
                        <v-form @submit.prevent="submit">
                           <v-text-field
                              prepend-icon=mdi-account
                              name="Username"
                              label="Username"
                              type="username"
                              placeholder="username"
                              v-model="inputs.username"
                              :error-messages="$store.state.auth.registration_error.username"
                           ></v-text-field>
                           <v-text-field
                              prepend-icon=mdi-account
                              name="First Name"
                              label="First Name"
                              type="username"
                              placeholder="firstname"
                              v-model="inputs.firstname"
                              :error-messages="$store.state.auth.registration_error.firstname"
                           ></v-text-field>
                           <v-text-field
                              prepend-icon=mdi-account
                              name="Last Name"
                              label="Last Name"
                              type="username"
                              placeholder="lastname"
                              v-model="inputs.lastname"
                              :error-messages="$store.state.auth.registration_error.lastname"
                           ></v-text-field>
                           <v-text-field
                              id="email"
                              prepend-icon=mdi-email
                              name="email"
                              label="Email"
                              type="email"
                              placeholder="email"
                              v-model="inputs.email"
                              :error-messages="$store.state.auth.registration_error.email"
                           ></v-text-field>
                           <v-text-field
                              id="password"
                              prepend-icon=mdi-lock
                              name="password"
                              label="Password"
                              type="password"
                              placeholder="password"
                              v-model="inputs.password1"
                              :error-messages="$store.state.auth.registration_error.password1"
                           ></v-text-field>
                           <v-text-field
                              id="password2"
                              prepend-icon=mdi-lock
                              name="password2"
                              label="Validate Password"
                              type="password"
                              placeholder="re-type password"
                              v-model="inputs.password2"
                              :error-messages="$store.state.auth.registration_error.password2"
                           ></v-text-field>
                           <v-btn
                              type="submit"
                              color="primary"
                              class="mr-4"
                              @click="createAccount(inputs)"
                              :loading="$store.state.auth.registrationLoading"
                            >
                              Create Account
                            </v-btn>
                        </v-form>
                     </v-card-text>
                    <router-link to="/login">return to login page</router-link>
                  </v-card>
               </v-flex>
            </v-layout>
         </v-container>
      </v-main>
   </v-app>
</template>

<script>
import { mapActions, mapState } from 'vuex';
export default {
  data() {
    return {
      inputs: {
        firstname: '',
        lastname: '',
        username: '',
        password1: '',
        password2: '',
        email: '',
      },
    };
  },
  computed: mapState('auth', [
    'registrationCompleted',
    'registrationError',
    'registrationLoading',
  ]),
  methods: {
    createAccount({ username, firstname, lastname, email, password1, password2 }) {
      this.$store.dispatch('auth/createAccount', { username, firstname, lastname, email, password1, password2 })
        .then(() => this.$router.push('/'));
    },
  },
  beforeRouteLeave(to, from, next) {
    this.clearRegistrationStatus();
    next();
  },
};
</script>

<style>
form input {
  display: block
}
.error {
  color: crimson;
  font-size: 12px;
}
</style>