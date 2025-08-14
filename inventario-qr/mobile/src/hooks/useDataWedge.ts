import { useState, useEffect } from 'react';
import { DeviceEventEmitter } from 'react-native';
import DataWedgeIntents from 'react-native-datawedge-intents';

// El nombre de la acción que configuraremos en DataWedge
const INTENT_ACTION = 'com.inventarioqr.SCAN';

interface ScanData {
  source: string;
  data: string;
  labelType: string;
}

export const useDataWedge = (callback: (data: ScanData) => void) => {
  useEffect(() => {
    // 1. Registrar el listener para los intents de DataWedge
    const subscription = DeviceEventEmitter.addListener(INTENT_ACTION, (intent) => {
        // DataWedge envía los datos en diferentes claves según la versión
        const data = intent['com.symbol.datawedge.data_string'] || intent.data;
        const source = intent['com.symbol.datawedge.source'] || 'unknown';
        const labelType = intent['com.symbol.datawedge.label_type'] || 'unknown';

        if (data) {
            callback({ data, source, labelType });
        }
    });

    // 2. Registrar la app para recibir los intents
    DataWedgeIntents.registerReceiver(INTENT_ACTION, "");

    // 3. Función de limpieza para eliminar el listener
    return () => {
      DeviceEventEmitter.removeAllListeners(INTENT_ACTION);
    };
  }, [callback]);
};
