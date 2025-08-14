import React from 'react';
import { View, Text, StyleSheet, FlatList, Button } from 'react-native';
import { useSelector } from 'react-redux';
import { RootState } from '../../src/store/store';

export default function BuscarNotaScreen() {
    // Mock data
    const searchResults = [
        { id: 'NOTA-001', date: '2024-08-14', items: 3, status: 'FINALIZADA' },
        { id: 'NOTA-002', date: '2024-08-15', items: 5, status: 'BORRADOR' },
    ];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Buscar Notas</Text>
      {/* Aquí iría un TextInput para la búsqueda */}
      <FlatList 
        data={searchResults}
        keyExtractor={(item) => item.id}
        renderItem={({item}) => (
            <View style={styles.itemContainer}>
                <Text>{item.id} ({item.status})</Text>
                <Text>{item.date} - {item.items} items</Text>
                <Button title="Ver/Editar" onPress={() => { /* Navegar a detalles */}} />
            </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
    container: { flex: 1, padding: 10 },
    title: { fontSize: 22, fontWeight: 'bold', marginBottom: 10 },
    itemContainer: { padding: 15, borderBottomWidth: 1, borderBottomColor: '#ccc' }
});
