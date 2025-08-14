import React, { useState } from 'react';
import { Text, View, StyleSheet, Button, Alert, TextInput, FlatList } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useDataWedge } from '../../src/hooks/useDataWedge';
import api from '../../src/services/api';

// Mock de los tipos que vendrían de Redux o schemas
interface Producto {
    codigo: string;
    descripcion: string;
}

interface NotaItem extends Producto {
    cantidad: number;
}

export default function ScannerScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const { solicitante, sucursal, almacen } = params;

  const [items, setItems] = useState<NotaItem[]>([]);
  const [lastScanned, setLastScanned] = useState<Producto | null>(null);
  const [quantity, setQuantity] = useState('1');

  const handleScan = async (scanData: { data: string }) => {
    console.log('Scan recibido:', scanData.data);
    try {
      const response = await api.get<Producto>(`/catalogo/${scanData.data}`);
      setLastScanned(response.data);
      Alert.alert('Producto Encontrado', response.data.descripcion);
    } catch (error) {
      Alert.alert('Error', `No se encontró el producto con código: ${scanData.data}`);
      setLastScanned(null);
    }
  };

  useDataWedge(handleScan);

  const handleAddItem = () => {
    if (!lastScanned) {
      Alert.alert('Error', 'No hay ningún producto escaneado para agregar.');
      return;
    }
    const cantidadNum = parseInt(quantity, 10);
    if (isNaN(cantidadNum) || cantidadNum <= 0) {
      Alert.alert('Cantidad inválida', 'Por favor, ingrese un número válido.');
      return;
    }

    // Lógica para agregar o actualizar item en la lista
    setItems(prevItems => {
        const existingItem = prevItems.find(item => item.codigo === lastScanned.codigo);
        if (existingItem) {
            return prevItems.map(item => 
                item.codigo === lastScanned.codigo 
                ? { ...item, cantidad: item.cantidad + cantidadNum } 
                : item
            );
        } else {
            return [...prevItems, { ...lastScanned, cantidad: cantidadNum }];
        }
    });

    // Limpiar para el siguiente escaneo
    setLastScanned(null);
    setQuantity('1');
  };
  
  const handleFinish = () => {
    // Aquí se guardaría la nota completa y se enviaría al API
    console.log("Finalizando nota:", {
        header: { solicitante, sucursal, almacen },
        items: items
    });
    Alert.alert('Nota Finalizada', 'La nota ha sido guardada y está lista para ser enviada.');
    // Navegar a la pantalla de búsqueda o home
    router.push('/(app)/home');
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>Solicitante: {solicitante}</Text>
        <Text style={styles.headerText}>Sucursal: {sucursal} / Almacén: {almacen}</Text>
      </View>

      <View style={styles.scanResult}>
        <Text style={styles.scanResultTitle}>Último escaneo:</Text>
        {lastScanned ? (
            <Text style={styles.scanResultText}>{lastScanned.descripcion} ({lastScanned.codigo})</Text>
        ) : (
            <Text style={styles.scanResultText}>Esperando escaneo...</Text>
        )}
        <View style={styles.quantityContainer}>
            <TextInput
                style={styles.input}
                value={quantity}
                onChangeText={setQuantity}
                keyboardType="numeric"
                placeholder="Cantidad"
            />
            <Button title="Agregar" onPress={handleAddItem} disabled={!lastScanned} />
        </View>
      </View>

      <FlatList
        data={items}
        keyExtractor={(item) => item.codigo}
        renderItem={({ item }) => (
            <View style={styles.listItem}>
                <Text style={styles.itemText}>{item.descripcion}</Text>
                <Text style={styles.itemText}>Cantidad: {item.cantidad}</Text>
            </View>
        )}
        ListHeaderComponent={<Text style={styles.listTitle}>Items en la Nota</Text>}
      />
      
      <Button title="Finalizar Nota" onPress={handleFinish} disabled={items.length === 0} />
    </View>
  );
}

const styles = StyleSheet.create({
    container: { flex: 1, padding: 10, backgroundColor: '#f5f5f5' },
    header: { padding: 10, backgroundColor: 'white', borderRadius: 5, marginBottom: 10 },
    headerText: { fontSize: 14, color: '#333' },
    scanResult: { padding: 15, backgroundColor: 'white', borderRadius: 5, marginBottom: 10 },
    scanResultTitle: { fontSize: 16, fontWeight: 'bold', marginBottom: 5 },
    scanResultText: { fontSize: 14, color: 'navy', marginBottom: 10 },
    quantityContainer: { flexDirection: 'row', alignItems: 'center' },
    input: { borderWidth: 1, borderColor: 'gray', padding: 10, borderRadius: 5, flex: 1, marginRight: 10 },
    listTitle: { fontSize: 18, fontWeight: 'bold', marginTop: 10, marginBottom: 5, paddingLeft: 5 },
    listItem: { flexDirection: 'row', justifyContent: 'space-between', padding: 15, backgroundColor: 'white', borderBottomWidth: 1, borderBottomColor: '#eee' },
    itemText: { fontSize: 14 },
});
