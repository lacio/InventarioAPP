import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Nota, NotaItem, Firma, NotaEncabezado } from '../../../common/types';

interface NotaState {
  currentNota: Nota | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: NotaState = {
  currentNota: null,
  isLoading: false,
  error: null,
};

const notaSlice = createSlice({
  name: 'nota',
  initialState,
  reducers: {
    startNewNota: (state, action: PayloadAction<NotaEncabezado>) => {
        state.currentNota = {
            id: `temp-id-${Date.now()}`,
            estado: 'BORRADOR',
            ...action.payload,
            items: [],
        };
        state.isLoading = false;
        state.error = null;
    },
    setNota: (state, action: PayloadAction<Nota>) => {
        state.currentNota = action.payload;
    },
    clearNota: (state) => {
        state.currentNota = null;
    },
    addItem: (state, action: PayloadAction<NotaItem>) => {
        if (state.currentNota) {
            const existingItem = state.currentNota.items.find(it => it.producto === action.payload.producto);
            if (existingItem) {
                // Update quantity if item exists
                existingItem.cantidad_entregada = action.payload.cantidad_entregada;
            } else {
                // Add new item
                state.currentNota.items.push(action.payload);
            }
        }
    },
    updateItemQuantity: (state, action: PayloadAction<{ producto: string; cantidad: number }>) => {
        if (state.currentNota) {
            const item = state.currentNota.items.find(it => it.producto === action.payload.producto);
            if (item) {
                item.cantidad_entregada = action.payload.cantidad;
            }
        }
    },
    removeItem: (state, action: PayloadAction<string>) => {
        if (state.currentNota) {
            state.currentNota.items = state.currentNota.items.filter(it => it.producto !== action.payload);
        }
    },
    setIntercompanyFlag: (state, action: PayloadAction<{ producto: string; intercompany: boolean; empresaOrigen?: string }>) => {
        if (state.currentNota) {
            const item = state.currentNota.items.find(it => it.producto === action.payload.producto);
            if (item) {
                item.intercompany = action.payload.intercompany;
                item.empresa_origen = action.payload.empresaOrigen;
            }
        }
    },
    setSignatures: (state, action: PayloadAction<Firma>) => {
        if (state.currentNota) {
            state.currentNota.firmas = action.payload;
        }
    }
  },
});

export const { 
    startNewNota,
    setNota, 
    clearNota, 
    addItem, 
    updateItemQuantity, 
    removeItem, 
    setIntercompanyFlag, 
    setSignatures 
} = notaSlice.actions;

export default notaSlice.reducer;
