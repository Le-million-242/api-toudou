<template>
  <div class="manager-dashboard-container">
    <h2>Manage Users</h2>
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.username }}
        <button @click="deleteUser(user.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: []
    };
  },
  async created() {
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/users', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    this.users = await response.json();
  },
  methods: {
    async deleteUser(userId) {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/users/${userId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        this.users = this.users.filter(user => user.id !== userId);  // Retirer l'utilisateur supprimé de la liste
      }
    }
  }
};
</script>

<style scoped>
/* Style pour le tableau de bord du manager */
.manager-dashboard-container {
  padding: 20px;
}

button {
  background-color: #f44336;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #d32f2f;
}

li {
  margin: 10px 0;
}
</style>
