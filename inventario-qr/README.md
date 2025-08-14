# Inventario QR – Salidas/Devoluciones + Intercompany

Monorepo con una aplicación mobile en React Native (Expo) y una API en FastAPI para gestionar un inventario con códigos QR, incluyendo lógica de negocio para traslados intercompany.

## Stack Tecnológico

- **Monorepo:** Estructura simple con directorios para `api`, `mobile` y `common`.
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy, Pydantic, Alembic.
- **Base de Datos:** PostgreSQL (gestionado con Docker).
- **Frontend:** React Native con Expo (TypeScript).
- **Gestión de Estado (Mobile):** Redux Toolkit.
- **Navegación (Mobile):** React Navigation.
- **Contenerización:** Docker y Docker Compose.

## Requerimientos Previos

- **Node.js** (v18+)
- **Python** (v3.11+)
- **Docker** y **Docker Compose**
- **Git**

## Cómo Empezar

Sigue estos pasos para levantar el entorno de desarrollo completo.

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd inventario-qr
```

### 2. Configurar Variables de Entorno

Copia el archivo de ejemplo y ajústalo si es necesario. Los valores por defecto están diseñados para funcionar con la configuración de Docker Compose.

```bash
cp .env.example .env
```

### 3. Levantar Backend y Base de Datos

Este comando construirá la imagen de la API, descargará la de Postgres y levantará ambos servicios. La API estará disponible en `http://localhost:8000`.

```bash
docker-compose up --build
```

La primera vez, Alembic creará las tablas automáticamente al iniciar la API.

### 4. Instalar Dependencias y Ejecutar la App Móvil

Abre una nueva terminal y navega al directorio de la aplicación móvil.

```bash
cd mobile

# Instalar dependencias
npm install
```

Una vez instaladas las dependencias, inicia el servidor de desarrollo de Expo.

```bash
# Iniciar la app
npx expo start
```

Esto abrirá el DevTools de Expo en tu navegador. Puedes:
- **Escanear el código QR** con la aplicación Expo Go en tu dispositivo móvil (iOS o Android).
- **Presionar `a`** para intentar abrir en un emulador de Android.
- **Presionar `i`** para intentar abrir en un simulador de iOS.

**Nota importante:** Para que la app móvil se comunique con tu API local, asegúrate de que tu dispositivo móvil esté en la misma red Wi-Fi que tu computadora. Es posible que necesites cambiar la URL de la API en `mobile/src/services/api.ts` de `localhost` a la dirección IP de tu máquina en la red local (ej: `http://192.168.1.100:8000`).

### 5. Probar la Aplicación

- **Usuario Demo:**
  - **Usuario:** `user@demo.com`
  - **Contraseña:** `demopass`

- **Flujo Básico:**
  1. Inicia sesión en la app móvil.
  2. Ve a la pestaña "Crear Nota" y presiona "Iniciar Escaneo".
  3. Escanea un código QR de producto (puedes generar uno con el valor `PROD001` o `PROD002`).
  4. La app debería mostrar la información del producto.
  5. (Lógica a implementar) Agrega el ítem a una lista de "borrador".
  6. (Lógica a implementar) Ve a la pantalla de firma, firma y guarda.
  7. (Lógica a implementar) Finaliza la nota.
  8. Verifica que se haya creado un PDF en la carpeta `generated_pdfs` del proyecto.
  9. Accede a `http://localhost:8000/notas/{ID_DE_LA_NOTA}/pdf` para descargar el comprobante.

## Estructura del Proyecto

```
/inventario-qr
  /api             # Backend en FastAPI
    /alembic         # Migraciones de base de datos
    /app             # Código fuente de la API
      /routers       # Endpoints de la API
      database.py    # Conexión a BD
      models.py      # Modelos de SQLAlchemy
      schemas.py     # Esquemas de Pydantic
      crud.py        # Lógica de acceso a datos
      ...            # Otros módulos (seguridad, PDF, etc.)
    Dockerfile
    requirements.txt
  /mobile          # App móvil en React Native (Expo)
    /app             # Pantallas y navegación (expo-router)
    /src             # Lógica de la app
      /services      # Cliente de API
      /store         # Redux store y slices
    package.json
  /common          # Tipos y utilidades compartidas
    /py              # Tipos de Pydantic para Python
    /ts              # Tipos de TypeScript para el móvil
  .editorconfig
  docker-compose.yml # Orquestación de servicios
  README.md          # Este archivo
  .env.example       # Plantilla de variables de entorno
```
