# Arquitectura del Sistema - Visión General

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                     ENTORNO DE PRUEBA                            │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐                    ┌──────────────────────┐
│    SISTEMA A         │                    │    SISTEMA B         │
│  (Inventario)        │                    │  (Pedidos)           │
│                      │                    │                      │
│  - REST API          │                    │  - XML API           │
│  - JSON Format       │                    │  - Legacy Style      │
│  - OpenAPI 3.0       │                    │  - Text Doc          │
│  - SQLite DB         │                    │  - SQLite DB         │
│  - Port 5001         │                    │  - Port 5002         │
│                      │                    │                      │
│  Endpoints:          │                    │  Endpoints:          │
│  GET /api/locations  │                    │  GET /api/orders     │
│  GET /api/inventory  │                    │  POST /api/stock/... │
│  POST /api/.../upd.. │                    │  GET /api/stock      │
└──────────────────────┘                    └──────────────────────┘
         ▲                                           ▲
         │                                           │
         │         ┌─────────────────┐              │
         │         │                 │              │
         └─────────┤   INTEGRACIÓN   ├──────────────┘
                   │   (Tu Código)   │
                   │                 │
                   │  - Transforma   │
                   │    JSON ↔ XML   │
                   │  - Sincroniza   │
                   │    Inventario   │
                   │  - Procesa      │
                   │    Pedidos      │
                   └─────────────────┘
```

## Flujo de Datos

### Flujo 1: Sincronización de Inventario (A → B)

```
1. Integración solicita inventario completo
   GET http://localhost:5001/api/inventory
   ↓
2. Sistema A responde con JSON:
   {
     "success": true,
     "data": [
       {
         "location_code": "STORE001",
         "sku": "SKU001",
         "product_name": "Laptop HP",
         "quantity": 5
       },
       ...
     ]
   }
   ↓
3. Integración agrupa por ubicación y convierte a XML:
   <stock_update>
     <location>
       <location_code>STORE001</location_code>
       <products>
         <product>
           <sku>SKU001</sku>
           <product_name>Laptop HP</product_name>
           <quantity>5</quantity>
         </product>
       </products>
     </location>
   </stock_update>
   ↓
4. Integración envía a Sistema B
   POST http://localhost:5002/api/stock/update
   Content-Type: application/xml
   ↓
5. Sistema B actualiza su caché de stock
```

### Flujo 2: Procesamiento de Pedidos (B → A)

```
1. Integración solicita pedidos pendientes
   GET http://localhost:5002/api/orders?status=pending
   ↓
2. Sistema B responde con XML:
   <orders_response>
     <orders>
       <item>
         <order_number>ORD-2024-001</order_number>
         <location_code>STORE001</location_code>
         <items>
           <item>
             <sku>SKU001</sku>
             <quantity>2</quantity>
           </item>
         </items>
       </item>
     </orders>
   </orders_response>
   ↓
3. Para cada item en cada pedido:
   Integración convierte a JSON y actualiza inventario:
   POST http://localhost:5001/api/inventory/update
   {
     "location_code": "STORE001",
     "sku": "SKU001",
     "quantity": 2,
     "operation": "decrement"
   }
   ↓
4. Sistema A decrementa el inventario
   ↓
5. Sistema A responde con resultado:
   {
     "success": true,
     "data": {
       "previous_quantity": 5,
       "new_quantity": 3
     }
   }
```

## Modelos de Datos

### Sistema A - Base de Datos

**Tabla: locations**
```
id | code      | name            | type
---+-----------+-----------------+----------
1  | WAREHOUSE | Almacén Central | warehouse
2  | STORE001  | Tienda Centro   | store
3  | STORE002  | Tienda Norte    | store
4  | STORE003  | Tienda Sur      | store
```

**Tabla: products**
```
id | sku    | name                    | description
---+--------+-------------------------+--------------------
1  | SKU001 | Laptop HP ProBook 450   | Laptop profesional...
2  | SKU002 | Mouse Logitech MX Ma... | Mouse inalámbrico...
...
```

**Tabla: inventory**
```
id | location_id | product_id | quantity
---+-------------+------------+----------
1  | 1           | 1          | 50
2  | 1           | 2          | 120
3  | 2           | 1          | 5
...
```

### Sistema B - Base de Datos

**Tabla: orders**
```
id | order_number | customer_name  | location_code | status  | order_date
---+--------------+----------------+---------------+---------+-------------
1  | ORD-2024-001 | María González | STORE001      | pending | 2024-01-15
...
```

**Tabla: order_items**
```
id | order_id | sku    | product_name            | quantity | unit_price
---+----------+--------+-------------------------+----------+------------
1  | 1        | SKU001 | Laptop HP ProBook 450   | 1        | 649.99
2  | 1        | SKU002 | Mouse Logitech MX Ma... | 2        | 49.99
...
```

**Tabla: stock_levels** (caché de Sistema A)
```
id | location_code | sku    | product_name  | quantity | last_updated
---+---------------+--------+---------------+----------+--------------
1  | STORE001      | SKU001 | Laptop HP ... | 5        | 2024-01-15...
...
```

## Transformaciones Requeridas

### 1. JSON (Sistema A) → XML (Sistema B)

**Entrada (JSON):**
```json
{
  "location_code": "STORE001",
  "sku": "SKU001",
  "product_name": "Laptop HP ProBook 450",
  "quantity": 5
}
```

**Salida (XML):**
```xml
<product>
  <sku>SKU001</sku>
  <product_name>Laptop HP ProBook 450</product_name>
  <quantity>5</quantity>
</product>
```

**Agrupamiento por ubicación:**
Múltiples productos de la misma ubicación deben agruparse bajo un elemento `<location>`.

### 2. XML (Sistema B) → JSON (Sistema A)

**Entrada (XML):**
```xml
<item>
  <sku>SKU001</sku>
  <quantity>2</quantity>
</item>
```

**Salida (JSON):**
```json
{
  "location_code": "STORE001",  // Del pedido
  "sku": "SKU001",
  "quantity": 2,
  "operation": "decrement"
}
```

## Consideraciones de Diseño

### Atomicidad
¿Qué pasa si un pedido tiene 3 items y el segundo falla?
- **Opción A:** Revertir todos los cambios (requiere tracking)
- **Opción B:** Continuar con los siguientes items, registrar error
- **Opción C:** Validar todo antes de hacer cambios

### Idempotencia
¿Se puede ejecutar la sincronización múltiples veces sin efectos secundarios?
- El Sistema B usa UPSERT (INSERT ... ON CONFLICT UPDATE)
- Esto permite idempotencia en la sincronización de inventario

### Manejo de Errores
Tipos de errores a considerar:
- **Red:** Timeout, conexión rechazada
- **Validación:** Ubicación no existe, SKU no encontrado
- **Negocio:** Stock insuficiente
- **Formato:** JSON/XML malformado

### Frecuencia de Sincronización
No es parte de la prueba, pero en un sistema real:
- Inventario: Cada 5-15 minutos (batch)
- Pedidos: Polling cada 1-2 minutos o webhook

## Tecnologías Utilizadas en los Sistemas

### Sistema A
- **Lenguaje:** Python 3.11
- **Framework:** Flask 3.0
- **Base de datos:** SQLite
- **Documentación:** OpenAPI 3.0 + Swagger UI
- **Despliegue:** Docker + Docker Compose

### Sistema B
- **Lenguaje:** Python 3.11
- **Framework:** Flask 3.0
- **Base de datos:** SQLite
- **Documentación:** Archivo de texto
- **Despliegue:** Docker + Docker Compose

## Testing

### Datos de Prueba Incluidos

**Ubicaciones:** 4 (1 almacén, 3 tiendas)
**Productos:** 8 SKUs
**Registros de inventario:** 32 (8 productos × 4 ubicaciones)
**Pedidos:** 6 (4 pendientes, 1 en proceso, 1 completado)
**Items en pedidos:** ~15 items en total

## Recursos Adicionales

- **Documentación Sistema A:** http://localhost:5001/docs
- **Documentación Sistema B:** `system-b/API_DOCUMENTATION.txt`
- **OpenAPI Spec:** http://localhost:5001/openapi.json
