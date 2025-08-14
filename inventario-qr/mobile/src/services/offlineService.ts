import AsyncStorage from '@react-native-async-storage/async-storage';
import { Nota } from '../../../common/types';

const DRAFTS_KEY = 'DRAFT_NOTES';
const CATALOG_CACHE_KEY = 'CATALOG_CACHE';

// --- Notas en Borrador ---

export const getLocalDrafts = async (): Promise<Nota[]> => {
  try {
    const jsonValue = await AsyncStorage.getItem(DRAFTS_KEY);
    return jsonValue != null ? JSON.parse(jsonValue) : [];
  } catch (e) {
    console.error('Error loading drafts from storage', e);
    return [];
  }
};

export const saveLocalDrafts = async (drafts: Nota[]): Promise<void> => {
  try {
    const jsonValue = JSON.stringify(drafts);
    await AsyncStorage.setItem(DRAFTS_KEY, jsonValue);
  } catch (e) {
    console.error('Error saving drafts to storage', e);
  }
};

// --- Cache del Catálogo de Productos ---

export const getCatalogCache = async (): Promise<Record<string, any>> => {
    try {
      const jsonValue = await AsyncStorage.getItem(CATALOG_CACHE_KEY);
      return jsonValue != null ? JSON.parse(jsonValue) : {};
    } catch (e) {
      console.error('Error loading catalog cache', e);
      return {};
    }
  };

export const saveProductToCache = async (product: { codigo: string, data: any }): Promise<void> => {
    try {
        const cache = await getCatalogCache();
        cache[product.codigo] = product.data;
        const jsonValue = JSON.stringify(cache);
        await AsyncStorage.setItem(CATALOG_CACHE_KEY, jsonValue);
    } catch (e) {
        console.error('Error saving product to cache', e);
    }
};