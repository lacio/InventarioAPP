export type EstadoNota = "BORRADOR" | "FINALIZADA";
export type EstadoRegularizacion = "PEND_REG" | "REG_OK";

export interface Firma {
  solicitante: string; // Base64 PNG
  entrega: string;     // Base64 PNG
}

export interface NotaItem {
  linea?: number;
  producto: string;
  descripcion: string;
  um: string;
  factor_empaque: number;
  cantidad_entregada: number;
  cantidad_devuelta?: number;
  requiere_lote: boolean;
  lote?: string | null;
  serie?: string | null;
  intercompany: boolean;
  empresa_origen?: string | null;
  estado_regularizacion?: EstadoRegularizacion | null;
  sc_numero?: string | null;
  motivo?: string | null;
  observacion?: string | null;
}

export interface Nota {
  id: string; // UUID
  estado: EstadoNota;
  empresa_solicitante: string;
  filial: string;
  almacen: string;
  centro_costo?: string | null;
  items: NotaItem[];
  firmas?: Firma | null;
  hash?: string | null;
  creado_por?: string;
}

// This is a simplified version for creating a note header
export interface NotaEncabezado {
    empresa_solicitante: string;
    filial: string;
    almacen: string;
    centro_costo?: string | null;
}
