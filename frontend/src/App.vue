<template>
  <div id="app">
    <nav>
      <router-link to="/chat" v-if="!isAuthenticated">MediAssistant</router-link>
      <router-link to="/login" v-if="!isAuthenticated">Login</router-link>
      <router-link to="/signup" v-if="!isAuthenticated">Signup</router-link>
      <router-link to="/chat" v-if="isAuthenticated">Medical Assistance</router-link>
      <button v-if="isAuthenticated" @click="logout" id="logout">Logout</button>
    </nav>
    <router-view />
  </div>
</template>


<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState(["token"]),
    isAuthenticated() {
      return !!this.token;
    },
  },
  methods: {
    logout() {
      this.$store.commit("logout"); // Ensure mutation is triggered
      this.$router.push("/login"); // Redirect after logout
    },
  },
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
}

#app {
  text-align: center;
  margin: 0;
  padding: 0;
}

nav {
  display: flex;
  justify-content: space-between; /* Distribute space between items */
  padding: 10px;
  background-color: #333;
  color: white;
  margin: 0;
  width: 100%; /* Ensure the navbar spans the full width */
  box-sizing: border-box; /* Include padding and border in the element's total width and height */
}

nav a {
  color: white;
  text-decoration: none;
  padding: 8px;
}

button {
  background-color: red;
  color: white;
  border: none;
  padding: 8px;
  cursor: pointer;
}

#logout {
  margin-left: auto; /* Push the logout button to the end of the nav */
  width: 5%;
  border-radius: 20px;
}
</style>