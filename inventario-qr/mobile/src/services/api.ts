import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Asegúrate de que esta URL apunta a tu API. Si usas un emulador de Android,
// puede ser 'http://10.0.2.2:8000'. Para un dispositivo físico en la misma red,
// usa la IP de tu máquina.
const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('jwt_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
