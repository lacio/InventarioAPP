import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../../src/services/api';

export default function LoginScreen() {
  const [username, setUsername] = useState('user@demo.com');
  const [password, setPassword] = useState('demopass');
  const router = useRouter();

  const handleLogin = async () => {
    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await api.post('/auth/login', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });

        const { access_token } = response.data;
        await AsyncStorage.setItem('jwt_token', access_token);
        router.replace('/(app)/home');
    } catch (error) {
        Alert.alert('Error de Login', 'Usuario o contraseña incorrectos.');
        console.error(error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Inventario QR</Text>
      <TextInput
        style={styles.input}
        placeholder="Usuario"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
      />
      <TextInput
        style={styles.input}
        placeholder="Contraseña"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title="Login" onPress={handleLogin} />
    </View>
  );
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'center', padding: 20 },
    title: { fontSize: 24, fontWeight: 'bold', textAlign: 'center', marginBottom: 20 },
    input: { borderWidth: 1, borderColor: 'gray', padding: 10, marginBottom: 12, borderRadius: 5 }
});
