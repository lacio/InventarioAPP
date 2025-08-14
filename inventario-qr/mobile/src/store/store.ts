import { configureStore } from '@reduxjs/toolkit';
import notaReducer from './notaSlice';

export const store = configureStore({
  reducer: {
    nota: notaReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
