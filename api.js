// src/services/api.js
import axios from 'axios';

const API_URL = 'http://192.168.96.128:8000';  // URL de ton backend FastAPI

// Exemple d'une requête pour obtenir la liste des tâches
export const getTasks = async () => {
  try {
    const response = await axios.get(`${API_URL}/tasks`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des tâches:', error);
    throw error;
  }
};

// Exemple pour créer une tâche
export const createTask = async (task) => {
  try {
    const response = await axios.post(`${API_URL}/tasks`, task);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la création de la tâche:', error);
    throw error;
  }
};

// Exemple pour authentifier un utilisateur
export const authenticateUser = async (user) => {
  try {
    const response = await axios.post(`${API_URL}/authenticate`, user);
    return response.data.token;
  } catch (error) {
    console.error('Erreur lors de l\'authentification:', error);
    throw error;
  }
};
