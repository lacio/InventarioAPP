# Proyecto: App Android de Gestión de Inventario con Integración a ERP Protheus

## Tipo de desarrollo
La app debe funcionar en un dispositivo TC26BK

---

## Objetivo
Digitalizar y agilizar el proceso de salida y devolución de materiales en los almacenes de Agrocentro, evitando errores de registro y reduciendo tiempos operativos.

---

## Funcionalidades clave

1. **Lectura de códigos QR**
   - Usar boton físico del dispositivo 
   - Decodificar información del producto (código, descripción, etc.).
   
2. **Formulario inicial**
   - Campos: Nombre del solicitante, Sucursal, Almacén.
   - Validación de datos obligatorios.

3. **Registro de salida de materiales**
   - Escanear QR → mostrar datos del producto.
   - Campo manual para ingresar cantidad.
   - Validación de código de producto contra base de datos ERP.
   - Almacenar en lista temporal hasta finalización.

4. **Edición y devoluciones**
   - Buscar notas de salida previas.
   - Editar cantidades (para devoluciones).
   - Guardar cambios antes del envío final.

5. **Generación de comprobante**
   - Crear comprobante de salida en PDF para poder enviar a una impresora wifi
   - Incluir campos para firma del solicitante y del responsable de almacén.
   - Opción para imprimir en impresoras térmicas Bluetooth o Wi-Fi.

6. **Envío al ERP**
   - Botón “Finalizar” para registrar la salida de forma definitiva en Protheus.

7. **Manejo de casos especiales (multiempresa)**
   - Si el repuesto pertenece a otra empresa del grupo → generar automáticamente **solicitud de compra** en Protheus para la transferencia entre empresas.

8. **Modo offline**
   - Guardar datos localmente cuando no hay conexión.
   - Sincronizar automáticamente cuando vuelva la conexión.
