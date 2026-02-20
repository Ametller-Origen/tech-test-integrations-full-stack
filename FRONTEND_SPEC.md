# Prueba Técnica Frontend - Monitor de Sincronización de Stock

## Descripción General

Como parte de la segunda fase de esta prueba técnica, deberás construir una aplicación web frontend que monitoree y gestione la sincronización de datos de inventario entre el Sistema A (Inventario) y el Sistema B (Pedidos).

## Contexto del Negocio

Los dos sistemas backend que has integrado en la Fase 1 necesitan mantener sus datos de stock sincronizados. El Sistema B (Pedidos) mantiene una caché de los niveles de stock del Sistema A (Inventario) para verificar disponibilidad de productos al procesar pedidos.

Tu aplicación frontend debe:
- Mostrar el estado de sincronización entre ambos sistemas
- Identificar discrepancias en los niveles de stock
- Permitir sincronización manual
- Alertar cuando los datos están desactualizados

## Requisitos Funcionales

### 1. Panel de Estado de Sincronización

**Ubicación:** Parte superior de la aplicación

**Elementos requeridos:**
- **Indicador de Estado** (badge/chip visual):
  - 🟢 "Sincronizado" - Todos los datos coinciden
  - 🟡 "Desincronizado" - Hay discrepancias detectadas
  - 🔴 "Error" - Último intento de sincronización falló
  - ⚪ "Desconocido" - Aún no se ha verificado

- **Información de Última Sincronización:**
  - Timestamp de última sincronización exitosa
  - Tiempo transcurrido (ej: "hace 15 minutos")
  - Indicador si los datos están obsoletos (>1 hora)

- **Estadísticas Resumidas:**
  - Total de productos monitoreados
  - Registros sincronizados
  - Registros con discrepancias
  - Registros solo en Sistema A (no sincronizados a B)

**Interacciones:**
- Botón "Verificar Estado" - Compara datos actuales de ambos sistemas
- Botón "Sincronizar Ahora" - Ejecuta sincronización manual (A → B)
- Indicador de carga durante operaciones

### 2. Tabla de Comparación de Stock

**Ubicación:** Área principal de la aplicación

**Columnas requeridas:**
1. **Ubicación** (location_code y nombre)
2. **SKU** del producto
3. **Nombre del Producto**
4. **Stock en Sistema A** (cantidad actual)
5. **Stock en Sistema B** (cantidad en caché)
6. **Diferencia** (A - B)
7. **Estado** (indicador visual)
8. **Última actualización en B** (timestamp)

**Características:**
- Ordenamiento por cualquier columna (ascendente/descendente)
- Filtros:
  - Por ubicación (dropdown multi-select)
  - Por estado (sincronizado / con discrepancia / solo en A)
  - Por búsqueda de texto (SKU o nombre de producto)
- Resaltado visual:
  - Verde claro: Sincronizado (diferencia = 0)
  - Amarillo: Discrepancia pequeña (|diferencia| ≤ 5)
  - Rojo claro: Discrepancia grande (|diferencia| > 5)
  - Gris: Solo en Sistema A (no existe en B)

**Datos a mostrar:**
- Mínimo 10 registros por página
- Paginación si hay más de 10 registros
- Scroll virtual opcional para mejor performance

**Información de productos solo en A:**
Mostrar productos que existen en Sistema A pero no han sido sincronizados a Sistema B con un indicador especial.

### 3. Controles de Sincronización

**Botón "Sincronizar Ahora":**
- Ubicación: Panel de estado superior
- Funcionalidad:
  - Lee todo el inventario del Sistema A
  - Transforma a formato XML
  - Envía al endpoint de actualización del Sistema B
  - Muestra progreso durante la operación
  - Al completar, actualiza la vista automáticamente

**Estados del botón:**
- Normal: "Sincronizar Ahora"
- Durante operación: "Sincronizando..." (deshabilitado, con spinner)
- Después de éxito: Muestra confirmación temporal
- Después de error: Muestra error temporal

**Feedback de operación:**
- Notificación tipo toast/snackbar al completar
- Éxito: "✓ Sincronización completada: 32 registros actualizados"
- Error: "✗ Error en sincronización: [mensaje de error]"
- Las notificaciones deben auto-desaparecer después de 5 segundos

### 4. Historial de Sincronización

**Ubicación:** Panel lateral o sección inferior

**Contenido:**
- Lista de las últimas 10 sincronizaciones
- Para cada entrada:
  - Timestamp (fecha y hora)
  - Estado (✓ Éxito / ✗ Error)
  - Registros procesados (ej: "32 registros")
  - Mensaje de error (si aplica)
  - Duración de la operación

**Formato:**
```
[14:35:22] ✓ Sincronización exitosa - 32 registros - 1.2s
[14:20:15] ✗ Error - Timeout de conexión
[14:05:10] ✓ Sincronización exitosa - 32 registros - 0.9s
```

**Características:**
- Se actualiza automáticamente al ejecutar nueva sincronización
- Persistencia local (localStorage) opcional
- Máximo 10 entradas (FIFO)

### 5. Alertas y Notificaciones

**Alerta de datos obsoletos:**
- Mostrar banner prominente cuando:
  - El timestamp de última actualización en Sistema B > 1 hora
  - O cuando no hay registro de última sincronización
- Mensaje: "⚠️ Advertencia: Los datos en Sistema B tienen más de 1 hora de antigüedad. Considera sincronizar."
- Botón de acción rápida: "Sincronizar Ahora"
- Debe ser dismissible pero reaparecer en siguiente verificación

**Alerta de discrepancias grandes:**
- Mostrar cuando hay productos con diferencia > 10 unidades
- Mensaje: "⚠️ Se detectaron X productos con discrepancias significativas (>10 unidades)"
- Botón: "Ver productos" (scroll/filtro a esos productos)

### 6. Actualización Automática (Opcional/Bonus)

**Auto-verificación:**
- Cada 60 segundos, verificar estado de sincronización
- Actualizar indicadores y timestamp automáticamente
- No recargar toda la tabla (solo si hay cambios)
- Indicador visual de "próxima actualización en X segundos"
- Toggle para habilitar/deshabilitar auto-refresh

## Requisitos Técnicos

### Stack Tecnológico

**Framework Frontend:** Libre elección
- React, Vue.js, Angular, Svelte, o vanilla JS
- Documenta tu elección en el README

**Estilo:** Libre elección
- CSS puro, Tailwind, Bootstrap, Material UI, Ant Design, etc.

**Construcción:**
- Debe incluir un build/dev server
- Instrucciones claras de instalación y ejecución

**Gestión de Estado:**
- Usa el patrón que prefieras
- Si es una app simple, `useState` es suficiente
- Para complejidad mayor, Redux/Vuex/Pinia es aceptable

### APIs a Consumir

**Sistema A (Inventario) - http://localhost:5001**
```javascript
// Obtener inventario completo
GET /api/inventory
Response: {
  "success": true,
  "data": [
    {
      "location_code": "STORE001",
      "location_name": "Tienda Centro",
      "location_type": "store",
      "sku": "SKU001",
      "product_name": "Laptop HP ProBook 450",
      "quantity": 5
    },
    // ... más registros
  ]
}
```

**Sistema B (Pedidos) - http://localhost:5002**
```xml
<!-- Obtener stock almacenado -->
GET /api/stock
Response (XML):
<?xml version="1.0"?>
<stock_response>
  <status>success</status>
  <count>32</count>
  <stock_levels>
    <item>
      <location_code>STORE001</location_code>
      <sku>SKU001</sku>
      <product_name>Laptop HP ProBook 450</product_name>
      <quantity>5</quantity>
      <last_updated>2024-01-15T14:30:00.123456</last_updated>
    </item>
    <!-- ... más items -->
  </stock_levels>
</stock_response>
```

```xml
<!-- Sincronizar stock -->
POST /api/stock/update
Content-Type: application/xml

Request:
<?xml version="1.0"?>
<stock_update>
  <location>
    <location_code>STORE001</location_code>
    <products>
      <product>
        <sku>SKU001</sku>
        <product_name>Laptop HP ProBook 450</product_name>
        <quantity>5</quantity>
      </product>
    </products>
  </location>
</stock_update>

Response:
<stock_update_response>
  <status>success</status>
  <message>Stock levels updated successfully</message>
  <records_updated>32</records_updated>
</stock_update_response>
```

### Transformación de Datos

**Parsing XML:**
Necesitarás parsear XML del Sistema B.

**Generación XML:**
Para sincronizar, necesitas generar XML desde JSON:
- Agrupa productos por ubicación
- Genera estructura XML correcta
- Envía con Content-Type: application/xml

**Ejemplo de transformación requerida:**
```javascript
// Datos de Sistema A (JSON)
[
  { location_code: "STORE001", sku: "SKU001", product_name: "Laptop", quantity: 5 },
  { location_code: "STORE001", sku: "SKU002", product_name: "Mouse", quantity: 15 },
  { location_code: "STORE002", sku: "SKU001", product_name: "Laptop", quantity: 3 }
]

// Debe convertirse a (XML):
<stock_update>
  <location>
    <location_code>STORE001</location_code>
    <products>
      <product><sku>SKU001</sku><product_name>Laptop</product_name><quantity>5</quantity></product>
      <product><sku>SKU002</sku><product_name>Mouse</product_name><quantity>15</quantity></product>
    </products>
  </location>
  <location>
    <location_code>STORE002</location_code>
    <products>
      <product><sku>SKU001</sku><product_name>Laptop</product_name><quantity>3</quantity></product>
    </products>
  </location>
</stock_update>
```

### Manejo de Errores

**Errores de red:**
- Timeout en requests (configura timeout de 10s)
- Sistema A o B no disponible
- Muestra mensaje claro al usuario
- No dejes la UI en estado de carga infinita

**Errores de parsing:**
- XML malformado del Sistema B
- JSON inválido del Sistema A
- Muestra error técnico en consola, mensaje amigable al usuario

**Errores de sincronización:**
- Sistema B rechaza la actualización
- Muestra el mensaje de error del servidor
- Permite reintentar

**Estados de carga:**
- Todos los requests deben mostrar indicador de carga
- Deshabilitar botones durante operaciones
- Indicador puede ser spinner, skeleton, o progress bar

### Responsive Design
No imprescindible, se valorará si se implementa para los siguientes casos (Mobile (<768px), Tablet (768-1028px)).

## Estructura de Proyecto Esperada

```
frontend-monitor/
├── README.md              # Instrucciones claras de instalación y ejecución
├── package.json           # Dependencias (si usas npm/yarn)
├── src/
│   ├── components/        # Componentes reutilizables
│   ├── services/          # API calls y lógica de datos
│   ├── utils/             # Helpers (XML parsing, formateo, etc.)
│   ├── App.js/vue/etc     # Componente principal
│   └── index.js/main.js   # Entry point
├── public/                # Assets estáticos
└── dist/                  # Build output (generado)
```

## Instrucciones de Entrega
Tu código puede estar disponible en el mismo fork que en la fase 1, no hace falta hacer un fork a parte.

### README.md debe incluir:

1. **Descripción breve** del proyecto
2. **Stack tecnológico** utilizado
3. **Prerequisitos** (Node.js version, etc.)
4. **Instalación:**
   ```bash
   npm install
   # o yarn install
   ```
5. **Ejecución en desarrollo:**
   ```bash
   npm run dev
   # o npm start
   ```
6. **Build para producción:**
   ```bash
   npm run build
   ```
7. **Acceso:** URL donde corre la app (ej: http://localhost:3000)
8. **Navegadores soportados**
9. **Decisiones de diseño** (opcional pero valorado)
10. **Limitaciones conocidas** (si las hay)

### Código:
- Código limpio y bien organizado
- Comentarios donde sea necesario
- Nombres descriptivos de variables y funciones
- Sin código comentado o archivos innecesarios

### Git (Opcional):
- Commits claros y descriptivos
- Un commit no es suficiente ("Initial commit" con todo)
- Commits incrementales muestran tu proceso

## Criterios de Evaluación

Tu solución será evaluada en:

### Funcionalidad
- Panel de estado funciona correctamente
- Tabla de comparación muestra datos correctos
- Sincronización funciona (A → B)
- Verificación de estado detecta discrepancias
- Historial se actualiza correctamente

### Calidad del Código
- Código limpio y organizado
- Estructura de componentes lógica
- Separación de responsabilidades
- Manejo apropiado de estado
- Código reutilizable

### UI/UX
- Diseño visual atractivo y profesional
- Usabilidad intuitiva
- Feedback visual apropiado
- Estados de carga claros

### Integración con APIs
- Parsing correcto de JSON y XML
- Generación correcta de XML para sincronización
- Manejo de errores de red
- Transformación de datos correcta

## Tiempo Estimado

**Duración sugerida:** 3-4 horas

**Distribución recomendada:**
- Setup y estructura: 20 min
- Integración con APIs: 60 min
- UI/Componentes principales: 90 min
- Sincronización y lógica: 45 min
- Pulido: 30 min
- Testing y documentación: 15 min

## Recursos

**Documentación de APIs:**
- Sistema A: http://localhost:5001/docs
- Sistema B: Ver `system-b/API_DOCUMENTATION.txt`

**Datos de prueba:**
- 4 ubicaciones
- 8 productos
- 32 registros de inventario

**Testing:**
- Puedes usar `system-a/reset_database.py` para resetear datos
- Puedes usar `system-b/reset_database.py` para limpiar el caché
- Modifica manualmente el inventario con el endpoint de actualización de Sistema A

## Preguntas Frecuentes

**P: ¿Puedo usar una librería de componentes?**
R: Sí, Material UI, Ant Design, Bootstrap, etc. son aceptables.

**P: ¿Debo implementar autenticación?**
R: No, los sistemas no requieren autenticación.

**P: ¿Qué hago si el Sistema B está vacío al inicio?**
R: Es esperado. Muestra que no hay datos y permite sincronizar.

**P: ¿Debo hacer que funcione sin los sistemas backend?**
R: No, puedes asumir que los sistemas A y B están corriendo.

**P: ¿Puedo usar TypeScript?**
R: Sí, totalmente aceptable y valorado.

**P: ¿Necesito tests?**
R: No son obligatorios, pero se valorarán positivamente.

**P: ¿Cuánto debe pesar visualmente el diseño?**
R: Debe ser funcional y profesional. No necesita ser "pixel perfect" pero sí presentable.

## ¡Buena suerte!

Si tienes problemas técnicos con los sistemas backend, consulta:
- `README.md` - Instrucciones de despliegue
- `QUICK_START.md` - Verificación de sistemas
- Logs de Docker: `docker-compose logs -f`

