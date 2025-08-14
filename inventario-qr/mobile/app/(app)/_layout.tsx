import React, { useEffect } from 'react';
import { Tabs } from 'expo-router';
import { FontAwesome } from '@expo/vector-icons';
import { useDataWedge } from '../../src/hooks/useDataWedge';
import { useDispatch } from 'react-redux';
import { processScannedData } from '../../src/store/notaSlice';

function AppTabsLayout() {
  const dispatch = useDispatch();
  const scan = useDataWedge(true); // Habilitar el listener de DataWedge

  useEffect(() => {
    if (scan) {
      console.log('SCAN DETECTED:', scan.data);
      // @ts-ignore - Thunk action
      dispatch(processScannedData(scan.data));
    }
  }, [scan, dispatch]);

  return (
    <Tabs screenOptions={{ headerShown: true }}>
      <Tabs.Screen
        name="home"
        options={{
          title: 'Crear Nota',
          tabBarIcon: ({ color }) => <FontAwesome size={28} name="plus-circle" color={color} />,
        }}
      />
      <Tabs.Screen
        name="buscar"
        options={{
          title: 'Buscar Nota',
          tabBarIcon: ({ color }) => <FontAwesome size={28} name="search" color={color} />,
        }}
      />
       <Tabs.Screen
        // Esta pantalla ya no es necesaria, la ocultamos.
        name="scanner"
        options={{ href: null, title: 'Escanear QR' }}
      />
    </Tabs>
  );
}

export default AppTabsLayout;
