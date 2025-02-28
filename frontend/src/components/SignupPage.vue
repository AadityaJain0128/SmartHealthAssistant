<template>
  <div class="signup-container">
    <h2>Signup</h2>
    <form @submit.prevent="signup">
      <input type="text" v-model="username" placeholder="Username" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit">Signup</button>
    </form>
    <p>Already have an account? <router-link to="/login">Login</router-link></p>
    
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async signup() {
      this.errorMessage = "";
      try {
        await this.$http.post("/signup", {
          username: this.username,
          password: this.password,
        });
        this.$router.push("/login");
      } catch (error) {
        if (error.response && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = "Signup failed. Please try again.";
        }
      }
    },
  },
};
</script>

<style>
.signup-container {
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
  font-size: 14px;
}
</style>
