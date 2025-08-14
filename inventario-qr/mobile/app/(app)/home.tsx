import React, { useState } from 'react';
import { View, Text, Button, StyleSheet, TextInput, Alert } from 'react-native';
import { useRouter } from 'expo-router';

// Esta pantalla será el punto de entrada para crear una nota.
// Desde aquí se navegará a la pantalla de escaneo.
export default function HomeScreen() {
  const router = useRouter();
  const [solicitante, setSolicitante] = useState('');
  const [sucursal, setSucursal] = useState('');
  const [almacen, setAlmacen] = useState('');

  const handleCreateNota = () => {
    if (!solicitante || !sucursal || !almacen) {
      Alert.alert('Campos incompletos', 'Por favor, complete todos los campos para continuar.');
      return;
    }

    // Aquí se podría crear el encabezado de la nota primero
    // y luego navegar al scanner.
    console.log("Creando nueva nota con los datos:", { solicitante, sucursal, almacen });

    // Pasamos los datos del encabezado a la pantalla del scanner
    router.push({
      pathname: '/(app)/scanner',
      params: { solicitante, sucursal, almacen },
    });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Nueva Nota de Salida</Text>
      <Text style={styles.subtitle}>Complete los datos para iniciar el registro.</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Nombre del solicitante"
        value={solicitante}
        onChangeText={setSolicitante}
      />
      <TextInput
        style={styles.input}
        placeholder="Sucursal"
        value={sucursal}
        onChangeText={setSucursal}
      />
      <TextInput
        style={styles.input}
        placeholder="Almacén"
        value={almacen}
        onChangeText={setAlmacen}
      />

      <Button title="Iniciar Escaneo" onPress={handleCreateNota} />
    </View>
  );
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'center', padding: 20 },
    title: { fontSize: 22, fontWeight: 'bold', marginBottom: 10, textAlign: 'center' },
    subtitle: { fontSize: 16, textAlign: 'center', color: 'gray', marginBottom: 20 },
    input: {
        borderWidth: 1,
        borderColor: 'gray',
        padding: 10,
        marginBottom: 12,
        borderRadius: 5,
        width: '100%',
    }
});
