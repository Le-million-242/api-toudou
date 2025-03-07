<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <input v-model="username" type="text" placeholder="Username" required />
      </div>
      <div>
        <input v-model="password" type="password" placeholder="Password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://localhost:8000/authenticate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username, password: this.password })
        });

        if (!response.ok) {
          throw new Error('Invalid credentials');
        }

        const data = await response.json();
        localStorage.setItem('token', data.token);  // Sauvegarder le token dans le stockage local
        this.$router.push('/dashboard');  // Rediriger vers le tableau de bord
      } catch (error) {
        this.errorMessage = error.message;
      }
    }
  }
};
</script>

<style scoped>
/* Style basique pour la page de connexion */
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>
