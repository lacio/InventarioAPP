Actúa como ingeniero full-stack senior. Genera un monorepo listo para correr para el proyecto “Inventario QR – Salidas/Devoluciones + Intercompany”. Entrega código completo por archivo (ruta + contenido), más un README con pasos de arranque. No incluyas credenciales. Lee variables desde .env.

1) Estructura del repo
bash
Copiar
Editar
/inventario-qr
  /mobile          # Expo React Native (TypeScript)
  /api             # FastAPI (Python 3.11+)
  /common          # Tipos compartidos y utilidades (TS/Python)
  .editorconfig
  docker-compose.yml
  README.md
  .env.example
2) Mobile (Expo React Native, TypeScript)
Usar Expo + React Navigation + Redux Toolkit (estado nota).

Pantallas:

LoginScreen (usuario/clave; guarda token JWT).

EncabezadoNotaScreen (empresa solicitante, sucursal, almacén, centro de costo opcional).

EscaneoQRScreen (expo-barcode-scanner; valida código contra /api/catalogo/{codigo}; captura cantidad; toggle “Tomar de otra empresa (SC intercompany)” cuando A=0 y B>0).

ListaBorradorScreen (ítems agregados, edición de cantidades, eliminación).

BuscarNotaScreen (buscar por número/QR para editar/devolver).

FirmaScreen (firma solicitante y quien entrega; react-native-signature-canvas).

ResumenFinalScreen (validaciones previas a Finalizar).

ImpresionScreen (muestra/descarga PDF generado por backend; opción compartir/imprimir).

Lógica:

Estado nota: { id, empresaSolicitante, filial, almacen, items[], estado, firmas }.

Funciones: validarQR, agregarItem, editarCantidad, marcarIntercompany(empresaOrigen), firmar(), finalizar().

Llamadas a API con Axios. Token en header Authorization: Bearer ....

Manejo offline básico: cache en AsyncStorage para notas BORRADOR (auto-restore si la app se cierra).

UI/UX: validaciones de cantidad, UM y factor de empaque; toasts de error.

3) API (FastAPI + Pydantic v2 + SQLAlchemy + Alembic)
Endpoints:

POST /auth/login → devuelve JWT (hardcode usuarios demo).

GET /catalogo/{codigo} → valida QR y trae descripción/UM/factor y si requiere lote/serie.

POST /notas → crea nota BORRADOR (encabezado).

POST /notas/{id}/items → agrega/edita ítem; admite flag intercompany y empresa_origen.

POST /notas/{id}/firmas → guarda firmas (PNG base64) de solicitante/entrega.

POST /notas/{id}/finalizar → validaciones de stock;

Ítems normales → crea movimiento de salida en ERP (stub erp.create_movimiento_salida) y marca nota FINALIZADA.

Ítems con intercompany=true → crea Solicitud de Compra en Empresa A con proveedor=Empresa B (stub erp.create_sc_intercompany), marca línea PEND_REG y retorna sc_numero.

Devuelve URL del PDF del comprobante final con QR y hash.

GET /notas/{id} → consulta nota;

GET /notas/{id}/pdf → descarga del PDF.

Modelos (staging, Postgres):

Encabezado nota → nota_id (UUID), estado (BORRADOR|FINALIZADA), fecha, empresa_solicitante, filial, almacen, centro_costo (nullable), creado_por, firmas_json, hash.

Detalle nota_item → nota_id, linea, producto, descripcion, um, factor_empaque, cantidad_entregada, cantidad_devuelta, requiere_lote, lote (nullable), serie (nullable), empresa_origen, intercompany (bool), estado_regularizacion (NULL|PEND_REG|REG_OK), sc_numero (nullable), motivo (nullable), observacion (nullable).

Índices útiles y claves foráneas.

Integración ERP (stubs en /api/erp_client.py):

create_movimiento_salida(nota, items) → retorna mov_numero.

create_sc_intercompany(nota, item) → retorna sc_numero.

Por ahora simular respuestas y registrar logs; leer URL y token del ERP desde .env.

Seguridad:

JWT simple (JWT_SECRET, JWT_EXPIRES_MIN).

Dependencias FastAPI para validar token en cada endpoint.

CORS habilitado para el host de Expo dev.

PDF del comprobante:

Generar con reportlab + qrcode (png) e incluir: logo (URL en .env), encabezado, líneas, totales por UM, firmas incrustadas y QR con {nota_id, hash}.

Guardar en /api/generated_pdfs/{nota_id}.pdf.

Logs JSON y manejo de errores: estructura clara con código, mensaje y trace id.

4) Common
common/types.ts y common/py/types.py: tipos compartidos para Nota, NotaItem, Estados, payloads de API.

Utilidad de hash HMAC (clave en env HMAC_SECRET) para firmar el ID de nota que se incluye en el QR.

5) Intercompany (reglas)
Si empresa A no tiene stock y B sí, permitir activar en el móvil “Tomar de B y generar SC A→B”.

En Finalizar:

Líneas normales → movimiento de salida.

Líneas intercompany → crear SC en A (proveedor=B), marcar PEND_REG y retornar sc_numero.

Comprobante: mostrar SC N° en líneas intercompany y leyenda “Pendiente regularización intercompany”.

Preparar job de conciliación (no implementarlo aún) para marcar REG_OK cuando la SC/OC/Factura cierren ciclo.

6) Validaciones
Código escaneado debe coincidir con ERP.

Stock en almacén; si sin stock en A y con stock en B → ofrecer intercompany.

UM y factor de empaque.

Lote/Serie si aplica.

Devoluciones: no superar lo entregado; guardar motivo.

7) QR (formato sugerido)
El QR de producto (etiqueta) puede contener JSON:

json
Copiar
Editar
{"prod":"CODIGO_ERP","desc":"Descripción","um":"UN","factor":1,"lote":null,"serie":null}
El QR del comprobante contiene { "nota_id": "...", "hash": "..." }.

8) Docker & Dev
docker-compose.yml con Postgres + API (uvicorn) y puertos expuestos; volumen para PDFs.

.env.example con:

DB_URL=postgresql+psycopg://postgres:postgres@db:5432/inventario

JWT_SECRET=changeme

HMAC_SECRET=changeme

ERP_API_URL=http://erp.local/api

ERP_API_TOKEN=changeme

PDF_LOGO_URL=https://mi-logo.png

ALLOWED_ORIGINS=http://localhost:19006

Scripts Makefile/npm para dev, lint, test.

Alembic inicial con migraciones para tablas.

9) Calidad
Backend: pytest con pruebas de finalizar() (caso normal e intercompany).

Lint: ruff + black.

Front: TS estricto, ESLint + Prettier.

10) README.md
Instrucciones claras:

Requerimientos (Node, Python, Docker).

cp .env.example .env (ajustar).

docker-compose up --build levanta db + api.

En /mobile: npm i, npx expo start.

Usuario demo para login.

Cómo probar flujo: crear nota, escanear, firmar, Finalizar, descargar PDF.

Entrega todo el código con rutas y contenidos completos, listo para compilar/ejecutar.