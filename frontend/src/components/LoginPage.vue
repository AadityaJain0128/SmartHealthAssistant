<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <input type="text" v-model="username" placeholder="Username" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <router-link to="/signup">Sign Up</router-link></p>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";
import { mapMutations } from "vuex";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    ...mapMutations(["setToken"]),
    async loginUser() {
      try {
        const response = await this.$http.post("/login", {
          username: this.username,
          password: this.password,
        });

        const token = response.data.access_token;
        this.setToken(token);
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

        this.$router.push("/chat");
      } catch (error) {
        this.errorMessage = error.response?.data?.error || "Login failed";
      }
    },
  },
};
</script>

<style>
.login-container {
  text-align: center;
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background: white;
  box-shadow: 0px 0px 10px gray;
  border-radius: 8px;
}
input {
  display: block;
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
