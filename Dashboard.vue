<template>
  <div class="dashboard-container">
    <h2>Your Tasks</h2>
    <ul>
      <li v-for="task in tasks" :key="task.id">
        <span>{{ task.title }} - {{ task.status }}</span>
        <button v-if="task.status !== 'completed'" @click="closeTask(task.id)">Close</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tasks: []
    };
  },
  async created() {
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/tasks', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    this.tasks = await response.json();
  },
  methods: {
    async closeTask(taskId) {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/tasks/${taskId}/close`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        this.tasks = this.tasks.filter(task => task.id !== taskId); // Retirer la tâche de la liste
      }
    }
  }
};
</script>

<style scoped>
/* Style basique pour le tableau de bord */
.dashboard-container {
  padding: 20px;
}

button {
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

li {
  margin: 10px 0;
}
</style>
